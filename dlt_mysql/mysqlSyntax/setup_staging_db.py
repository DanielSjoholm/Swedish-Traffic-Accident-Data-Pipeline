import mysql.connector
from mysql.connector import Error


def create_mysql_db():
    try:
        # kopplar upp sig mot mySQL servern
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'
        )

        # skapar en cursor som används för att utföra SQL queries
        cursor = connection.cursor()

        # skapar en databas om den inte redan finns med namnet CRUD
        cursor.execute("CREATE DATABASE IF NOT EXISTS TRAFFIC_STAGING")
        cursor.execute("USE TRAFFIC_STAGING")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trafikverket_data (
            id VARCHAR(255) PRIMARY KEY);
        ''')

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()