import requests
import os
from dotenv import load_dotenv
from helpers.connect_db import connect_db, close_db

load_dotenv()

def _get_trafikverket_data():
    api_key = os.getenv('API_KEY')
    url = 'https://api.trafikinfo.trafikverket.se/v2/data.json'

    payload = """
    <REQUEST>
        <LOGIN authenticationkey='{}' />
        <QUERY objecttype='Situation' schemaversion='1.5'>
            <INCLUDE>Deviation</INCLUDE>
        </QUERY>
    </REQUEST>
    """.format(api_key)
    
    response = requests.post(url, data=payload, headers={'Content-Type': 'text/xml'})

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Misslyckades med att hämta data: {response.status_code}")
        print(response.text)
        return None

def table_exists(table_name):
    """Kontrollerar om en tabell finns i databasen."""
    conn, cur = connect_db()
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'staging' 
            AND table_name = %s
        );
    """, (table_name,))
    exists = cur.fetchone()[0]
    close_db(conn, cur)
    return exists

def get_existing_ids():
    """Hämtar alla existerande ID:n från trafikverket_data-tabellen om den finns."""
    if table_exists('trafikverket_data'):
        conn, cur = connect_db()
        cur.execute("SELECT id FROM staging.trafikverket_data")
        existing_ids = {row[0] for row in cur.fetchall()}
        close_db(conn, cur)
        return existing_ids
    else:
        print("Tabellen staging.trafikverket_data finns inte.")
        return set()

def trafikverket_resource():
    data = _get_trafikverket_data()
    existing_ids = get_existing_ids()  # Hämta alla redan existerande ID:n, om tabellen finns

    if data:
        for result in data['RESPONSE']['RESULT']:
            for situation in result['Situation']:
                for deviation in situation['Deviation']:
                    deviation_id = deviation.get('Id')
                    if deviation_id not in existing_ids:
                        yield deviation