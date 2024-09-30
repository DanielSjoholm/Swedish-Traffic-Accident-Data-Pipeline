def add_unique_constraint(conn, cur):
    """Lägger till unikhetsbegränsning på id-kolumnen i trafikverket_data-tabellen i schema staging."""
    try:
        cur.execute("""
            ALTER TABLE staging.trafikverket_data
            ADD CONSTRAINT unique_id UNIQUE(id);
        """)
        conn.commit()
        print("Unikhetsbegränsning har lagts till på id-kolumnen.")
    
    except Exception as e:
        print(f"Fel när unikhetsbegränsningen skulle läggas till: {e}")
        conn.rollback()