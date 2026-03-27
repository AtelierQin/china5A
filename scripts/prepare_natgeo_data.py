import json
import urllib.request
import urllib.parse
import time
import os

# National Geographic: 50 Places of a Lifetime (Global)
natgeo_world = [
    # Cities
    "Barcelona, Spain", "Hong Kong", "Istanbul, Turkey", "Jerusalem", "London, UK", 
    "New York City, USA", "Paris, France", "Rio de Janeiro, Brazil", "San Francisco, USA", "Venice, Italy",
    # Wild Places
    "Antarctica", "Amazon Rainforest, Brazil", "Canadian Rockies, Canada", "Galapagos Islands, Ecuador", 
    "Grand Canyon, USA", "Australian Outback", "Papua New Guinea Reefs", "Sahara Desert", 
    "Serengeti, Tanzania", "Tepuis, Venezuela",
    # Paradise
    "Amalfi Coast, Italy", "Boundary Waters, USA", "British Virgin Islands", "Greek Islands", 
    "Hawaii, USA", "Kyoto, Japan", "Kerala, India", "Palau", "Torres del Paine, Chile", "Seychelles",
    # Country Unbound
    "Alps, Switzerland", "Big Sur, USA", "Canadian Maritimes", "Coastal Norway", "Danang, Vietnam", 
    "Lake District, UK", "Loire Valley, France", "North Island, New Zealand", "Tuscany, Italy", "Vermont, USA",
    # World Wonders
    "Acropolis, Greece", "Angkor Wat, Cambodia", "Great Wall of China", "Machu Picchu, Peru", 
    "Mesa Verde, USA", "Petra, Jordan", "Pyramids of Giza, Egypt", "Taj Mahal, India", 
    "Vatican City", "Chichen Itza, Mexico"
]

# Chinese National Geography: 50 Places of a Lifetime in China
natgeo_china = [
    "万里长城", "故宫", "布达拉宫", "兵马俑", "莫高窟", "云冈石窟", "龙门石窟",
    "九寨沟", "黄龙", "喀纳斯", "青海湖", "纳木错", "泸沽湖", "赛里木湖", "西湖", "洱海",
    "珠穆朗玛峰", "梅里雪山", "贡嘎雪山", "南迦巴瓦峰", "冈仁波齐峰", "泰山", "黄山", "华山",
    "雅鲁藏布大峡谷", "怒江大峡谷", "长江三峡", "虎跳峡", "太鲁阁大峡谷",
    "呼伦贝尔大草原", "锡林郭勒草原", "伊犁拉提草原", "巴音布鲁克草原",
    "宁夏沙湖", "巴丹吉林沙漠", "塔克拉玛干沙漠", "鸣沙山月牙泉",
    "婺源", "丹巴藏寨", "平遥古城", "丽江古城", "凤凰古城", "乌镇", "西递宏村",
    "张家界", "桂林山水", "武夷山", "三亚", "神农架", "长白山"
]

def geocode(place_name):
    # Use OpenStreetMap Nominatim API
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(place_name)}&format=json&limit=1"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'China5A-Tracker/1.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0:
                return {
                    "lat": float(data[0]["lat"]),
                    "lng": float(data[0]["lon"]),
                    "display_name": data[0]["display_name"]
                }
    except Exception as e:
        print(f"Error geocoding {place_name}: {e}")
    
    return None

def generate_data(places_list, prefix):
    results = []
    for i, place in enumerate(places_list):
        print(f"Geocoding [{i+1}/{len(places_list)}]: {place}")
        geo = geocode(place)
        
        item = {
            "id": f"{prefix}_{i+1}",
            "name": place,
            "category": prefix,
            "location": geo["display_name"] if geo else "Location Unknown",
            "lat": geo["lat"] if geo else 0.0,
            "lng": geo["lng"] if geo else 0.0,
            "image": f"https://placehold.co/600x400?text={urllib.parse.quote(place)}"
        }
        results.append(item)
        time.sleep(1.1) # Respect OSM API rate limits (1 sec per request)
        
    return results

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    print("--- Generating NatGeo World 50 ---")
    world_data = generate_data(natgeo_world, "natgeo_world")
    with open(os.path.join(data_dir, 'natgeo_world.json'), 'w', encoding='utf-8') as f:
        json.dump(world_data, f, ensure_ascii=False, indent=2)
        
    print("\n--- Generating NatGeo China 50 ---")
    china_data = generate_data(natgeo_china, "natgeo_china")
    with open(os.path.join(data_dir, 'natgeo_china.json'), 'w', encoding='utf-8') as f:
        json.dump(china_data, f, ensure_ascii=False, indent=2)
        
    print("\nData generation complete! Files saved to data/ directory.")
