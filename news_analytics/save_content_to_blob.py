from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from secrets_config import *
from azure_config import *
from yle_get_content import *

connection_string = storage_account_connection_string()

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = get_news_container_name()

container_client = blob_service_client.get_container_client(container_name)

news_url = "https://yle.fi/a/74-20116807"
text_to_upload = get_content(news_url)

metadata = {
    "url": news_url
    }

blob_client = container_client.get_blob_client(news_url.split("/")[-1])

blob_client.upload_blob(text_to_upload, overwrite=True, metadata=metadata)

print(f"Text uploaded to {container_name}/{news_url} successfully.")
