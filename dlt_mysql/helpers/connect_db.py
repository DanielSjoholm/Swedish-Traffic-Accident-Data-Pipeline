import mysql.connector
import time

def connect_to_database(Database):
    """Skapar en connection till databasen och returnerar den"""
    try:
        config = {
            'host': 'localhost',
            'database': Database,
            'user': 'root',
            'password': 'password',
        }

        connection = mysql.connector.connect(**config)

        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        print(f'Error: {err}. Could not connect to database')
        time.sleep(5)
        return None