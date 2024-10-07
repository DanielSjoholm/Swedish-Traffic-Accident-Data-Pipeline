def create_schema(conn, cur):
    """Skapar en tabell som lagrar JSONB-data."""
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS staging;
    """)
    conn.commit()