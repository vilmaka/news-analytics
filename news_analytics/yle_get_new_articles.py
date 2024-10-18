from secrets_config import *
from azure.data.tables import TableServiceClient, TableEntity
from yle_web_requests import article_exist
from azure.storage.queue import QueueServiceClient

def yle_get_new_content(batchsize: int):
    connection_string = storage_account_connection_string()
    table_name = "latestarticle"
    queue_name = "article-urls"
    
    service = TableServiceClient.from_connection_string(conn_str=connection_string)
    queue_service = QueueServiceClient.from_connection_string(conn_str=connection_string)
    
    table_client = service.get_table_client(table_name)
    queue_client = queue_service.get_queue_client(queue_name)
    
    try:
        retrieved_entity = table_client.get_entity(partition_key="yle", row_key="")
        print("Entity retrieved successfully:")
        print(retrieved_entity["latest"])
    
        url = "https://yle.fi/a/74-" + str(retrieved_entity["latest"] + batchsize)
    
        if article_exist(url):
            for i in range(1, batchsize+1):
                queue_client.send_message("https://yle.fi/a/74-" + str(retrieved_entity["latest"] + i))
            retrieved_entity["latest"] += batchsize
            table_client.update_entity(retrieved_entity)
    
    except Exception as e:
        print(f"An error occurred: {e}")


yle_get_new_content(2)

