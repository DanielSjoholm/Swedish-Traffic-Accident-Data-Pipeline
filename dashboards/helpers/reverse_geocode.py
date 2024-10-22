import time
from geopy.geocoders import GoogleV3
from dotenv import load_dotenv
import json
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
geolocator = GoogleV3(api_key=GOOGLE_API_KEY)
cache_filename = "geocode_cache_lan.json"

def reverse_geocode(lat, lon, retries=3):
    try:
        with open(cache_filename, 'r') as cache_file:
            geocode_cache = json.load(cache_file)
    except FileNotFoundError:
        geocode_cache = {}

    cache_key = f"{lat},{lon}"
    
    # Kontrollera om koordinaterna redan finns i cachen
    if cache_key in geocode_cache:
        return geocode_cache[cache_key]  # Returnera från cachen
    
    for attempt in range(retries):
        try:
            location = geolocator.reverse((lat, lon))
            if location:
                address = location.address
                county = location.raw.get('address_components', [])
                lan = None
                
                for component in county:
                    if 'administrative_area_level_1' in component['types']:  # Län nivå
                        lan = component['long_name']
                        break
                
                if not lan:
                    lan = 'Ingen län hittad'
                
                geocode_cache[cache_key] = {'address': address, 'lan': lan}
                
                with open(cache_filename, "w") as cache_file:
                    json.dump(geocode_cache, cache_file, indent=4)
                
                return geocode_cache[cache_key]
            else:
                return None
        except Exception as e:
            print(f"Fel vid geokodning för {lat}, {lon} (försök {attempt+1}/{retries}): {e}")
            time.sleep(1)
    return None