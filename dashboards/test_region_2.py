import json
from geopy.geocoders import GoogleV3
from Connect_and_query import query_trafic_situations
from dotenv import load_dotenv
import os
import pandas as pd
import time

# Ladda API-nyckeln från .env-filen
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Filnamn för cachen
cache_filename = "geocode_cache_lan.json"
# Försök ladda cache från en fil
try:
    with open(cache_filename, "r") as cache_file:
        geocode_cache = json.load(cache_file)
except FileNotFoundError:
    geocode_cache = {}

# Funktion för att omvandla koordinater till adress och cacha resultatet
def reverse_geocode(lat, lon, retries=3):
    # Skapa en strängnyckel för cachen
    cache_key = f"{lat},{lon}"
    
    # Kontrollera om koordinaterna redan finns i cachen
    if cache_key in geocode_cache:
        return geocode_cache[cache_key]  # Returnera från cachen
    
    for attempt in range(retries):
        try:
            # Om inte, gör en ny API-förfrågan
            location = geolocator.reverse((lat, lon))
            if location:
                address = location.address
                # Extrahera län från location.raw om tillgängligt
                county = location.raw.get('address_components', [])
                lan = None
                
                for component in county:
                    if 'administrative_area_level_1' in component['types']:  # Län nivå
                        lan = component['long_name']
                        break
                
                if not lan:
                    lan = 'Ingen län hittad'
                
                # Lägg till i cachen
                geocode_cache[cache_key] = {'address': address, 'lan': lan}
                
                # Returnera och spara till cachen
                return geocode_cache[cache_key]
            else:
                return None
        except Exception as e:
            print(f"Fel vid geokodning för {lat}, {lon} (försök {attempt+1}/{retries}): {e}")
            time.sleep(1)  # Vänta innan omförsök
    return None

# Hämta data
df = query_trafic_situations()

# Ändra alla kolumnnamn till stora bokstäver
df.columns = df.columns.str.upper()

# Använd din Google API-nyckel här
geolocator = GoogleV3(api_key=GOOGLE_API_KEY)

# Räknare för ogiltiga koordinater
invalid_coord_count = 0
save_frequency = 100  # Spara varje 100:e iteration

# Iterera genom DataFrame och bearbeta varje rad
for index, row in df.iterrows():
    lat = row['WGS84_POINT_LATITUDE']
    lon = row['WGS84_POINT_LONGITUDE']
    
    if pd.notna(lat) and pd.notna(lon):
        result = reverse_geocode(lat, lon)
        if result:
            address = result['address']
            lan = result['lan'] if result['lan'] else 'Ingen län hittad'
            print(f"Koordinater: {lat}, {lon} -> Adress: {address}, Län: {lan}")
        else:
            print(f"Koordinater: {lat}, {lon} -> Ingen adress hittad")
    else:
        invalid_coord_count += 1
        print(f"Ogiltiga koordinater för rad {index}")
    
    # Lägg till en fördröjning för att undvika att överskrida API-kvoten
    time.sleep(0.15)
    
    # Spara cachen oftare (varje 100:e rad)
    if index % save_frequency == 0:
        with open(cache_filename, "w") as cache_file:
            json.dump(geocode_cache, cache_file, indent=4)
        print(f"Cache sparad vid rad {index}")

# Spara slutligen cachen efter sista iterationen
with open(cache_filename, "w") as cache_file:
    json.dump(geocode_cache, cache_file, indent=4)

# Skriv ut antal ogiltiga koordinater
print(f"Antal rader med ogiltiga koordinater: {invalid_coord_count}")