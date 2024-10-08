import os
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI
from secrets_config import *

connection_string = storage_account_connection_string()
news_container_name = "news-text"
news_blob_name = "art-2000010717534.txt"
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


news_content = fetch_blob_content(connection_string, news_container_name, news_blob_name)
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

print(response.choices[0].text)