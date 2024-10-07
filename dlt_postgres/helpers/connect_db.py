import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
    
        )
        cur = conn.cursor()
        print("Anslutning till databasen lyckades.")
        return conn, cur
    except psycopg2.DatabaseError as e:
        print(f"Fel vid anslutning till databasen: {e}")
        return None, None

def close_db(conn, cur):
    """Stänger anslutningen och kursorn."""
    if cur:
        cur.close()
    if conn:
        conn.close()
        print("Anslutningen stängdes.")

connect_db()