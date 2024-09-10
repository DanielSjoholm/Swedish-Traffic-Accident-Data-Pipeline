import os
from dotenv import load_dotenv
import snowflake.connector

# Ladda in lösenord från .env-filen
load_dotenv()

main_user = os.getenv('MAIN_USER')
main_password = os.getenv('MAIN_PASSWORD')
host = os.getenv('HOST')

db_password = os.getenv('DB_PASSWORD')

# Anslut till Snowflake
conn = snowflake.connector.connect(
    user = main_user,
    password = main_password,
    account = host,
)

# SQL för att skapa användare
create_user_sql = f"""
CREATE USER DLT_USER PASSWORD = '{db_password}'
DEFAULT_ROLE = 'DLT_ROLE'
MUST_CHANGE_PASSWORD = FALSE;
"""

# Exekvera SQL
cursor = conn.cursor()
cursor.execute(create_user_sql)

# Stäng anslutningen
cursor.close()
conn.close()

print("User created successfully!")
