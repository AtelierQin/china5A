import json
import os

filepath = os.path.join(os.path.dirname(__file__), '..', 'src', 'attractions.json')

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# The National Geographic 50 Places of a Lifetime includes some places already in China 5A
# Let's add them to both categories if they match, and set default category for others to ["5A"]
natgeo_matches = ["故宫博物院", "八达岭长城（八达岭-慕田峪长城）", "秦始皇帝陵博物院(兵马俑)", "黄山风景区", "布达拉宫景区"]

max_id = 0

for item in data:
    if item['id'] > max_id:
        max_id = item['id']
    if 'categories' not in item:
        item['categories'] = ["5A"]
    
    # Add NatGeo category if it matches our list
    if item['name'] in natgeo_matches and "NatGeo" not in item['categories']:
        item['categories'].append("NatGeo")

# Add some exclusive NatGeo destinations to demonstrate the feature
natgeo_exclusive = [
    {
        "id": max_id + 1,
        "name": "科罗拉多大峡谷 (Grand Canyon)",
        "location": "美国 亚利桑那州",
        "lat": 36.1069,
        "lng": -112.1129,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Grand_Canyon_Colorado_River_2013.jpg/960px-Grand_Canyon_Colorado_River_2013.jpg",
        "description": "国家地理“一生值得去的50个地方”之一，世界自然遗产。",
        "categories": ["NatGeo"]
    },
    {
        "id": max_id + 2,
        "name": "巴黎 (Paris)",
        "location": "法国 巴黎",
        "lat": 48.8566,
        "lng": 2.3522,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/960px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg",
        "description": "国家地理“一生值得去的50个地方”之一，世界浪漫之都。",
        "categories": ["NatGeo"]
    },
    {
        "id": max_id + 3,
        "name": "泰姬陵 (Taj Mahal)",
        "location": "印度 阿格拉",
        "lat": 27.1751,
        "lng": 78.0421,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Taj_Mahal_in_March_2004.jpg/960px-Taj_Mahal_in_March_2004.jpg",
        "description": "国家地理“一生值得去的50个地方”之一，世界文化遗产。",
        "categories": ["NatGeo"]
    },
    {
        "id": max_id + 4,
        "name": "南极洲 (Antarctica)",
        "location": "南极洲",
        "lat": -82.8628,
        "lng": 135.0000,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Antarctica_6400px_from_Blue_Marble.jpg/960px-Antarctica_6400px_from_Blue_Marble.jpg",
        "description": "国家地理“一生值得去的50个地方”之一，地球上最后的净土。",
        "categories": ["NatGeo"]
    }
]

# Only append if they haven't been added yet (run script idempotently)
existing_names = [item['name'] for item in data]
for item in natgeo_exclusive:
    if item['name'] not in existing_names:
        data.append(item)

# Save back
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Data updated successfully! Total records: {len(data)}")
