def create_schema(conn, cur):
    """Skapar en tabell som lagrar JSONB-data."""
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS staging;

        CREATE TABLE IF NOT EXISTS staging.trafikverket_data (
            id VARCHAR(255) PRIMARY KEY
        );
    """)
    conn.commit()
    print("Schema och tabell för JSON-data skapades.")