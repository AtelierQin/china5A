import urllib.request
import json
import re

url = "https://zh.wikipedia.org/w/api.php?action=parse&page=%E5%9B%BD%E5%AE%B65A%E7%BA%A7%E6%97%85%E6%B8%B8%E6%99%AF%E5%8C%BA&format=json&prop=wikitext"
req = urllib.request.Request(url, headers={'User-Agent': 'China5A-Tracker/2.0 (hq@example.com)'})

print("Fetching Wikipedia data...")
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        wikitext = data['parse']['wikitext']['*']
except Exception as e:
    print("Error fetching from Wikipedia API:", e)
    exit(1)

with open("/tmp/wiki_5a.txt", "w", encoding="utf-8") as f:
    f.write(wikitext)
print("Wikitext saved.")
