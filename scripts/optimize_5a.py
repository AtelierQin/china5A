import json
import re

with open('src/attractions.json', 'r', encoding='utf-8') as f:
    attractions = json.load(f)

# Group by the content inside parenthesis if it exists at the end of the name
groups = {}
singles = []

# To correctly match groups:
# e.g., "一大纪念馆（中国共产党一大·二大·四大纪念馆景区）"
# "慕田峪长城旅游景区（八达岭-慕田峪长城）"
for attr in attractions:
    name = attr['name']
    m = re.search(r'（([^）]+)）$', name)
    if m:
        parent_name = m.group(1)
        if parent_name not in groups:
            groups[parent_name] = []
        groups[parent_name].append(attr)
    else:
        singles.append(attr)

optimized = []
optimized.extend(singles)

# Process groups: if a group has only 1 item, it's just a regular name with a parenthesis suffix
# If a group has > 1 item, we merge them into a single attraction using the parent_name
for parent_name, items in groups.items():
    if len(items) == 1:
        optimized.append(items[0])
    else:
        print(f"Merging {len(items)} items for: {parent_name}")
        for i in items:
            print(f"  - {i['name']}")
            
        merged = items[0].copy()
        merged['name'] = parent_name
        # Keep the coordinates of the first item
        # Keep the id of the first item, discard the others
        optimized.append(merged)

# Sort by id to maintain order
optimized.sort(key=lambda x: x['id'])

print(f"Original items: {len(attractions)}")
print(f"Optimized items: {len(optimized)}")

with open('src/attractions.json', 'w', encoding='utf-8') as f:
    json.dump(optimized, f, ensure_ascii=False, indent=2)

print("Saved optimized attractions back to src/attractions.json")
