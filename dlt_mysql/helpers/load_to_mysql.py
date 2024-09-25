import json
from mysql.connector import Error
from helpers.connect_db import connect_to_database

def insert_dynamic_data_to_mysql(deviation_data):
    try:
        # Anslut till MySQL
        connection = connect_to_database('TRAFFIC_STAGING')
        cursor = connection.cursor()

        # Skapa en lista över alla unika kolumner från alla avvikelser
        all_columns = set()
        for deviation in deviation_data:
            all_columns.update(deviation.keys())

        # Säkerställ att alla kolumner finns i databasen
        for column in all_columns:
            cursor.execute(f"SHOW COLUMNS FROM trafikverket_data LIKE '{column}'")
            result = cursor.fetchone()

            # Om kolumnen inte finns, skapa den
            if not result:
                alter_query = f"ALTER TABLE trafikverket_data ADD COLUMN {column} TEXT"
                cursor.execute(alter_query)

        # Skapa INSERT-satsen dynamiskt baserat på alla unika kolumner
        column_names = ", ".join(all_columns)
        placeholders = ", ".join(["%s"] * len(all_columns))

        insert_query = f"INSERT INTO trafikverket_data ({column_names}) VALUES ({placeholders})"

        # Förbered datan att infogas
        for deviation in deviation_data:
            values = []
            for column in all_columns:
                # Lägg till värde om det finns, annars None
                value = deviation.get(column, None)
                if isinstance(value, (list, dict)):
                    values.append(json.dumps(value))  # Konvertera listor och dictionaries till JSON-sträng
                else:
                    values.append(value)

            cursor.execute(insert_query, tuple(values))

        # Committa förändringarna
        connection.commit()

    except Error as e:
        print(f"Error while inserting to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()