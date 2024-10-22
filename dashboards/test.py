import json

with open ('geocode_cache_lan.json', 'r') as cache_file:
    geocode_cache = json.load(cache_file)

    
print(len(geocode_cache))