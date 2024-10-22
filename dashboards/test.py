import json

# Ladda cachen från fil
with open('geocode_cache_lan.json', 'r') as cache_file:
    geocode_cache = json.load(cache_file)

# Initiera räknaren utanför loopen
counter = 0

# Iterera över nyckel och värde i cachen
for key, value in geocode_cache.items():
    if 'Stockholm' in value['lan']:  # Kontrollera om 'Stockholm' finns i länets namn
        counter += 1

# Skriv ut antal gånger 'Stockholm' hittades
print(counter)