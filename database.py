from basse import  create_vectors , retrieve_indexes
from postgresSQL import insert_data,fetch_data,create_connection,create_table
from typing import List

# Postgres configuration
dbname = "vectordata" #replace with your database name
user = "postgres" #replace with your username
password = "12345678" #replace with your password
host = "localhost" #or your host
port = "5432" #default port
tablename = "textdata" #table name

conn=create_connection(dbname,user,password, host, port)

def check_or_create_table(table_name=tablename):
    """
    Checks if a table exists in the 'public' schema.
    If it doesn't, creates it with default columns.

    Args:
        conn: psycopg2 connection object
        table_name (str): table to check/create

    Returns:
        bool: True if table exists (or is successfully created), False if error
    """
    default_columns = {
        "id": "SERIAL PRIMARY KEY",
        "data": "TEXT",
    }

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
            """, (table_name,))
            exists = cur.fetchone()[0]

        if not exists:
            create_table(conn, table_name, default_columns)
            print(f"✅ Table '{table_name}' was missing and is now created.")
        else:
            print(f"✅ Table '{table_name}' already exists.")
        return True

    except Exception as e:
        print(f"⚠️ Error checking/creating table '{table_name}': {e}")
        return False

def store_data(data:str) -> None:
    """Stores the text data as Vectors for future use.

    Args:
        data (str): The string containing what you have learnt from user.

    Returns:
        Nothing.
    """
    text_data = create_vectors(data)
    config_data = {"data":text_data}
    insert_data(conn,tablename,config_data)


def fetch_relevant_data(queries:List[str]) ->List[str]:
    """Retrieves the relevant data on basis of question from Vector Database.

    Args:
        queries (list): The list of questions you want to ask.

    Returns:
        list: List of answers to the questions.
    """
    relevant_data = []
    data = retrieve_indexes(queries)
    if isinstance(data,list):
        for i in data:
            for answer in i:
                q = f"Select data FROM {tablename} where id = {answer}; "
                relevant_data.append(fetch_data(conn,tablename,q))
        return relevant_data
    else:
        return data

