import json
from collections import Counter

# Läsa in JSON-filen
with open('geocode_cache_lan.json') as f:
    data = json.load(f)

# Räkna förekomster av varje län
lan_counts = Counter(entry['lan'] for entry in data.values())

# Skriva ut resultatet
for lan, antal in lan_counts.items():
    print(f"{lan}: {antal} st")