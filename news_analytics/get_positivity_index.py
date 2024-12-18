import os
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI
from convert_base64 import convert_from_base64
from secrets_config import *
import psycopg2
from azure.storage.queue import QueueServiceClient
from sql_features import *
import json

connection_string = storage_account_connection_string()
news_container_name = "news-text"
prompt_container_name = "prompt"
prompt_blob_name = "prompt.txt"

def fetch_blob_content(connection_string, container_name, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob()
        content = blob_data.readall().decode('utf-8')
        return content

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def analyze_content(news_url, news_content):
    prompt_content = fetch_blob_content(connection_string, prompt_container_name, prompt_blob_name)

    client = AzureOpenAI(
        api_key=openapi_key(),
        api_version="2024-02-01",
        azure_endpoint="https://news-project-ai-eus.openai.azure.com/"
    )

    deployment_name = "gpt35turbo"

    prompt = prompt_content.replace("{CONTENT}", news_content)

    response = client.completions.create(
        model=deployment_name,
        prompt=prompt,
        temperature=0,
        max_tokens=1,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    insert_positivity_index_to_sql(news_url, int(response.choices[0].text))

def analyze_next_batch():
    queue_service_client = QueueServiceClient.from_connection_string(storage_account_connection_string())
    queue_client = queue_service_client.get_queue_client("downloaded-articles")

    messages = queue_client.receive_messages(max_messages=2)
    for message in messages:
        article_json = convert_from_base64(message.content)
        article = json.loads(article_json)
        analyze_content(article["url"], article["content"])

