import requests
import os
from dotenv import load_dotenv
from mysqlSyntax.setup_staging_db import create_mysql_db
from helpers.load_to_mysql import insert_dynamic_data_to_mysql

load_dotenv()

def _get_trafikverket_data():
    api_key = os.getenv('API_KEY')
    url = 'https://api.trafikinfo.trafikverket.se/v2/data.json'

    payload = f"""
    <REQUEST>
        <LOGIN authenticationkey='{api_key}' />
        <QUERY objecttype='Situation' schemaversion='1.5'>
            <INCLUDE>Deviation</INCLUDE>
        </QUERY>
    </REQUEST>
    """
    
    response = requests.post(url, data=payload, headers={'Content-Type': 'text/xml'})

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Misslyckades med att hämta data: {response.status_code}")
        print(response.text)
        return None

def trafikverket_resource():
    data = _get_trafikverket_data()

    if data:
        deviations = []
        for result in data['RESPONSE']['RESULT']:
            for situation in result['Situation']:
                for deviation in situation['Deviation']:
                    deviations.append(deviation)

        # Infoga all data i MySQL-databasen
        insert_dynamic_data_to_mysql(deviations)

if __name__ == "__main__":
    create_mysql_db()
    trafikverket_resource()
    print("Datan har laddats in i MySQL-databasen.")