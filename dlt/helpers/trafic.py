# helpfunctions/trafikverket.py

import requests
import os
from dotenv import load_dotenv

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

def trafikverket_resource():
    data = _get_trafikverket_data()

    if data:
        for result in data['RESPONSE']['RESULT']:
            for situation in result['Situation']:
                for deviation in situation['Deviation']:
                    yield deviation