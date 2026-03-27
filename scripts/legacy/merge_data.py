import json
import csv

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return []

def load_poi_data(path):
    poi_map = {}
    try:
        # standard utf-8-sig handles BOM
        with open(path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
            
            # Find the header line
            header_idx = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('POI_ID'):
                    header_idx = i
                    break
            
            print(f"Header found at line {header_idx}: {lines[header_idx].strip()[:50]}...")
            
            reader = csv.DictReader(lines[header_idx:])
            for row in reader:
                # Basic validation
                if not row.get('景区名称'):
                    continue
                    
                name = row['景区名称']
                try:
                    poi_map[name] = {
                        'lat': float(row['POI_Latitude']),
                        'lng': float(row['POI_Longitude']),
                        'city': row.get('二级行政区划(Adm2)', ''),
                        'province': row.get('一级行政区划(Adm1)', '')
                    }
                except ValueError:
                    continue 

    except Exception as e:
        print(f"Error loading CSV: {e}")
    return poi_map

import re

def normalize_name(name):
    # 1. Remove standard suffixes
    suffixes = [
        "旅游景区", "风景名胜区", "旅游度假区", "旅游区", "风景区", "景区", 
        "国家森林公园", "森林公园", "国家湿地公园", "湿地公园", "地质公园", "公园",
        "博物馆", "纪念馆", "故居", "旧址", "大峡谷", "文化旅游区", "生态旅游区",
        "旅游", "风景", "陵", "古镇", "瀑布", "文化园" # Added more
    ]
    
    clean_name = name
    for suffix in suffixes:
        clean_name = clean_name.replace(suffix, "")
        
    # Remove common geographic prefixes often found in official names
    prefixes = [
        "北京市", "天津市", "上海市", "重庆市",
        "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省", "江苏省", 
        "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省", 
        "湖北省", "湖南省", "广东省", "海南省", "四川省", "贵州省", 
        "云南省", "陕西省", "甘肃省", "青海省", "台湾省",
        "内蒙古自治区", "广西壮族自治区", "西藏自治区", "宁夏回族自治区", "新疆维吾尔自治区",
        "内蒙古", "广西", "西藏", "宁夏", "新疆", "香港", "澳门",
        "北京", "天津", "上海", "重庆", "南京", "苏州", "无锡", "常州", "扬州", "徐州",
        "杭州", "宁波", "温州", "绍兴", "嘉兴", "湖州", "金华", "台州",
        "合肥", "黄山", "福州", "厦门", "南昌", "九江", "济南", "青岛", "郑州", "洛阳",
        "武汉", "宜昌", "十堰", "长沙", "广州", "深圳", "珠海", "南宁", "桂林",
        "成都", "贵阳", "昆明", "丽江", "西安", "兰州", "西宁", "银川", "乌鲁木齐"
    ]
    for prefix in prefixes:
        clean_name = clean_name.replace(prefix, "")
        
    # Generic City removal: Remove "Start + XX市"
    # Matches 2-5 chinese chars followed by 市 at start
    clean_name = re.sub(r'^[\u4e00-\u9fa5]{2,5}市', '', clean_name)
    # Generic Discrict/County removal: "XX县", "XX区" matches at start
    clean_name = re.sub(r'^[\u4e00-\u9fa5]{2,5}[区县州盟]', '', clean_name)
    
    return clean_name

def find_best_match(target_name, poi_map):
    # 1. Exact match
    if target_name in poi_map:
        return poi_map[target_name]
    
    target_core = normalize_name(target_name)
    
    candidates = []
    for poi_name, data in poi_map.items():
        # Exact match of cores
        poi_core = normalize_name(poi_name)
        
        if poi_core == target_core and len(poi_core) > 1: # Avoid matching single char
            candidates.append((100, data)) # High priority
        elif poi_core in target_core and len(poi_core) > 1:
            candidates.append((len(poi_core), data))
        elif target_core in poi_core and len(target_core) > 1:
            candidates.append((len(target_core), data))
            
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    
    return None

import urllib.parse

def main():
    print("Loading data...")
    # 1. Load Data
    current_attractions = load_json('src/attractions.json')
    official_list = load_json('data/data_5a.json')
    poi_map = load_poi_data('data/scenic_poi.csv')
    
    print(f"Loaded {len(current_attractions)} existing items.")
    print(f"Loaded {len(official_list)} official 5A items.")
    print(f"Loaded {len(poi_map)} POI coordinates.")

    final_list = []
    processed_names = set()
    next_id = 1

    # 1. Add existing items (Top 20) -> DISABLED for full rebuild
    # for item in current_attractions:
    #     final_list.append(item)
    #     # Normalize name for tracking
    #     processed_names.add(item['name'])
    #     if item['id'] >= next_id:
    #         next_id = item['id'] + 1
            
    # 2. Process official list
    added_count = 0
    skipped_count = 0
    
    for item in official_list:
        raw_name = item['name']
        
        # Clean name ("Provice City Spot" -> "Spot") is hard, so we rely on substring match
        # Check if already processed (fuzzy check)
        is_processed = False
        for p_name in processed_names:
            if p_name in raw_name or raw_name in p_name:
                is_processed = True
                break
        if is_processed:
            continue

        # Find coordinate
        match = find_best_match(raw_name, poi_map)
        
        if match:
            encoded_name = urllib.parse.quote(raw_name)
            new_item = {
                "id": next_id,
                "name": raw_name,
                "location": f"{match['province']} {match['city']}",
                "lat": match['lat'],
                "lng": match['lng'],
                "image": f"https://placehold.co/600x400?text={encoded_name}", 
                "description": f"位于{match['province']}{match['city']}的国家5A级旅游景区。"
            }
            final_list.append(new_item)
            processed_names.add(raw_name)
            next_id += 1
            added_count += 1
        else:
            print(f"SKIPPED: {raw_name}")
            skipped_count += 1

    print(f"Merged complete. Total items: {len(final_list)}")
    print(f"Added: {added_count}, Skipped: {skipped_count}")

    # Write result
    with open('src/attractions.json', 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
