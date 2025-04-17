import psycopg2

def create_connection(dbname, user, password, host, port):
    """Creates and returns a PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def create_table(conn, table_name, columns):
    """Creates a table in the PostgreSQL database."""
    try:
        cur = conn.cursor()
        column_definitions = ", ".join([f"{col_name} {data_type}" for col_name, data_type in columns.items()])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"
        cur.execute(create_table_query)
        conn.commit()
        print(f"Table '{table_name}' created successfully.")
        cur.close()
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")

def insert_data(conn, table_name, data):
    """Inserts data into the specified table."""
    try:
        cur = conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        cur.execute(insert_query, values)
        conn.commit()
        print("Data inserted successfully.")
        cur.close()
    except psycopg2.Error as e:
        return (f"Error inserting data: {e}")

def fetch_data(conn, table_name, query="SELECT * FROM {}"):
    """Fetches data from the specified table."""
    try:
        cur = conn.cursor()
        cur.execute(query.format(table_name))
        rows = cur.fetchall()
        cur.close()
        return rows
    except psycopg2.Error as e:
        return f"Error fetching data: {e}"

def close_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()
        print("Connection closed.")

# Example Usage:

# # Database credentials (replace with your actual credentials)
# dbname = "vectordata" #replace with your database name
# user = "postgres" #replace with your username
# password = "12345678" #replace with your password
# host = "localhost" #or your host
# port = "5432" #default port
# #
# # Connect to the database
# conn = create_connection(dbname, user, password, host, port)
# column = {
#     "id": "SERIAL PRIMARY KEY",
#     "data":"TEXT",
# }
# tablename = "textdata" #table name
# # create_table(conn,table_name=tablename,columns=column)
# dataa = {
#     "data":"hello"
# }
# insert_data(conn,table_name=tablename,data=dataa)
# conn.close()

