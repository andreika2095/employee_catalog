import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        dbname="ILINE",
        user="postgres",
        password="postgres",
        host="localhost",
        cursor_factory=RealDictCursor
    )