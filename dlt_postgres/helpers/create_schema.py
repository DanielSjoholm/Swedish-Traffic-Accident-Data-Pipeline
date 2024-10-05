def create_schema(conn, cur):
    """Skapar en tabell som lagrar JSONB-data."""
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS staging;
    """)

    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS warhouse;
    """)

    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS mart;
    """)
    
    conn.commit()