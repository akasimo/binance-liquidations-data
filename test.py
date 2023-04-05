import os
import psycopg2
from dotenv import load_dotenv


# Load the environment variables from the .env file
load_dotenv()

# Read the environment variables
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']
POSTGRES_DB = os.environ['POSTGRES_DB']

# Create the connection string
conn_str = f"dbname='{POSTGRES_DB}' user='{POSTGRES_USER}' password='{POSTGRES_PASSWORD}' host='{POSTGRES_HOST}' port='{POSTGRES_PORT}'"

# Test the connection and list table names
try:
    conn = psycopg2.connect(conn_str)
    print("Connection to the PostgreSQL server is successful.")
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    table_names = cursor.fetchall()
    
    print("Table names:")
    for table_name in table_names:
        print(table_name[0])

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
