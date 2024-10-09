import requests
from bs4 import BeautifulSoup
import json

def get_content(url: str):
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
    content_json = json_data['pageData']['article']['content']
    content_string = ""

    for text in content_json:
        if text["type"] == "text":
            content_string += text["text"]
    return content_string