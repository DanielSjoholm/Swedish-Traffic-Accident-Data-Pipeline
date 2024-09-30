# helpfunctions/trafikverket.py
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

def flatten_json(y):
    """Rekursivt platta ut JSON till en enkel nivå."""
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def get_existing_ids():
    """Hämtar alla existerande ID:n från trafikverket_data-tabellen."""
    conn, cur = connect_db()
    cur.execute("SELECT id FROM staging.trafikverket_data")
    existing_ids = {row[0] for row in cur.fetchall()}
    close_db(conn, cur)
    return existing_ids

def trafikverket_resource():
    data = _get_trafikverket_data()
    existing_ids = get_existing_ids()  # Hämta alla redan existerande ID:n

    if data:
        for result in data['RESPONSE']['RESULT']:
            for situation in result['Situation']:
                for deviation in situation['Deviation']:
                    deviation_id = deviation.get('Id')
                    if deviation_id not in existing_ids:
                        # Platta ut JSON-strukturen
                        flat_deviation = flatten_json(deviation)
                        yield flat_deviation