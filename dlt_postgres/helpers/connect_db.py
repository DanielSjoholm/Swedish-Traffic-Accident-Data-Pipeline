import psycopg2

def connect_db():
    try:
        conn = psycopg2.connect("dbname=traffic_analytics_db user=postgres password=password host=localhost")
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