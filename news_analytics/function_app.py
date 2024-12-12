import datetime
import logging
from tkinter import INSERT
import azure.functions as func
from yle_get_new_articles import *
from yle_web_requests import *
import random
from secrets_config import *
from get_positivity_index import *
from sql_features import *

app = func.FunctionApp()

@app.function_name(name="checkNewArticles")
@app.timer_trigger(schedule="0 * * * * *", arg_name="mytimer", run_on_startup=True) 
def test_function(mytimer: func.TimerRequest) -> None:
    batchsize = random.randint(10,20)
    yle_get_new_content(batchsize)
    logging.info("Executed timer")

@app.queue_trigger(arg_name="msg", queue_name="article-urls", connection="storageAccountConnectionString")
@app.queue_output(arg_name="outputQueueItem", queue_name="downloaded-articles", connection="storageAccountConnectionString")
def test_function(msg: func.QueueMessage, outputQueueItem: func.Out[str]) -> None:
    article = yle_get_parsed_content(msg.get_body().decode('utf-8'))
    if article == None:
        return
    if article.lang == "fi":
        outputQueueItem.set(json.dumps(article.to_dict()))
        insert_tags(article.url, article.tags)
        insert_article_info(article.url, article.title, article.date)
        print("Queing article.")

@app.function_name(name="AnalyzeArticles")
@app.timer_trigger(schedule="0 * * * * *", arg_name="mytimer", run_on_startup=True) 
def test_function(mytimer: func.TimerRequest) -> None:
    analyze_next_batch()