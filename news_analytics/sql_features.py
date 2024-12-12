import psycopg2
from secrets_config import *

#Insert the positivity index row to database.

def get_connection():
    return psycopg2.connect(
    dbname='news-data',
    user=sql_username(),
    password=sql_password(),
    host='news-sql.postgres.database.azure.com',
    port='5432'
    )

def insert_rows(insert_query, data_to_insert, insert_many):
    conn = get_connection()
    transaction = conn.cursor()
    try:
        if insert_many:
            transaction.executemany(insert_query, data_to_insert)
        else:
            transaction.execute(insert_query, data_to_insert)
    
        conn.commit()
    
        print("Row inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        transaction.close()
        conn.close()

def insert_positivity_index_to_sql(news_url, positivity_index):    
    insert_query = """
    INSERT INTO news_scale (id, index_column)
    VALUES (%s, %s);
    """
    data_to_insert = (news_url, positivity_index)
    insert_rows(insert_query, data_to_insert, False)


def insert_tags(news_url, tags):
    insert_query = """
    INSERT INTO news_tags (id, tag)
    VALUES (%s, %s);
    """
    data_to_insert = []
    for tag in tags:
        data_to_insert.append((news_url, tag))
    insert_rows(insert_query, data_to_insert, True)

def insert_article_info(news_url, title, date):
    insert_query = """
    INSERT INTO news_info (id, title, date)
    VALUES (%s, %s, %s);
    """
    data_to_insert = (news_url, title, date)
    insert_rows(insert_query, data_to_insert, False)


