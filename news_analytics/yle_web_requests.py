import requests
from bs4 import BeautifulSoup
import json
from article import Article

def yle_get_parsed_content(url: str) -> Article:
    response = requests.get(url)
    
    if response.status_code == 200:
        html_content = response.text
    else:
        return None
    
    page = BeautifulSoup(html_content, 'html.parser')
    body = page.body
    script_elements = body.find_all('script')
    

    script_text = script_elements[-1].string.removeprefix('window.__INITIAL__STATE__=')
    json_data = json.loads(script_text)
    content = get_content_string(json_data)
    title = get_title(json_data)
    language = get_language(json_data)
    tags = get_tags(json_data)
    
    return Article(url, title, content, language, tags)

def get_content_string(json_data):
    content_json = json_data['pageData']['article']['content']
    content_string = ""
    
    for text in content_json:
        if text["type"] == "text":
            content_string += text["text"]
    return content_string

def get_title(json_data):
    return json_data["pageData"]["article"]["headline"]["full"]

def get_language(json_data):
    return json_data["pageData"]["article"]["language"]

def get_tags(json_data):
    tags = []
    tags_json = json_data["pageData"]["article"]["mainMedia"][0]["tags"]

    for tag in tags_json:
        for label in tag["label"]:
            if label["language"] == "fin":
                tags.append(label["value"])

    return tags


def article_exist(url: str):
    response = requests.get(url)
        
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise Exception(f"Received status code: {response.status_code}")

yle_get_parsed_content("https://yle.fi/a/74-20117600")
