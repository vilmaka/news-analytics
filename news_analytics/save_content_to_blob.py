from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from secrets_config import *
from azure_config import *
from yle_get_content import *

# Replace with your Azure Storage account connection string
connection_string = storage_account_connection_string()

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Specify the container name
container_name = get_news_container_name()

# Create a container if it doesn't exist
container_client = blob_service_client.get_container_client(container_name)

# Specify the blob name and the text to upload
news_url = "https://yle.fi/a/74-20116807"
text_to_upload = get_content(news_url)

metadata = {
    "url": news_url
    }

# Create a BlobClient
blob_client = container_client.get_blob_client(news_url.split("/")[-1])

# Upload the text
blob_client.upload_blob(text_to_upload, overwrite=True, metadata=metadata)

print(f"Text uploaded to {container_name}/{news_url} successfully.")
