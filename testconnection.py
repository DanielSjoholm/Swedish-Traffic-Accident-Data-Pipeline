import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
# API-endpoint för trafikolycksdata
url = 'https://api.trafikinfo.trafikverket.se/v2/data.json'

# Request payload med XML förfrågan för att hämta olycksdata
payload = """
<REQUEST>
    <LOGIN authenticationkey='{}' />
    <QUERY objecttype='Situation' schemaversion='1.5'>
        <INCLUDE>Deviation</INCLUDE>
    </QUERY>
</REQUEST>
""".format(api_key)

# Skicka API-anropet
response = requests.post(url, data=payload, headers={'Content-Type': 'text/xml'})

# Kontrollera om anropet lyckades
if response.status_code == 200:
    data = response.json()
    # Spara datan till en JSON-fil
    with open('trafikolyckor.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
else:
    print(f"Misslyckades med att hämta data: {response.status_code}")
    print(response.text)
