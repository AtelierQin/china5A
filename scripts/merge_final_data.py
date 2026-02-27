import json
import csv
import re
import os

def normalize(name):
    """Normalize name for easier matching."""
    return re.sub(r'[（\(].*?[）\)]', '', name).strip()

def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_csv(filepath):
    poi_data = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        # Skip the first metadata line
        next(f)
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('景区名称', '')
            if name:
                poi_data[name] = row
    return poi_data

def main():
    print("Loading data...")
    wiki_list = load_json('data/wiki_attractions.json')
    current_data = load_json('src/attractions.json')
    poi_data = load_csv('data/scenic_poi.csv')
    
    # Create a map of current data by name for easy lookup
    current_map = {item['name']: item for item in current_data}
    
    # Create CSV lookup maps
    csv_exact_map = poi_data
    csv_norm_map = {normalize(k): v for k, v in poi_data.items()}
    csv_names = list(poi_data.keys())

    final_list = []
    
    print(f"Processing {len(wiki_list)} attractions from Wikipedia...")
    
    count_existing = 0
    count_csv_exact = 0
    count_csv_partial = 0
    count_missing_loc = 0

    for idx, name in enumerate(wiki_list, 1):
        entry = {
            "id": idx,
            "name": name,
            "location": "", # Default empty
            "lat": None,
            "lng": None,
            "image": f"https://placehold.co/600x400?text={name}", # Default placeholder
            "description": f"位于中国的国家5A级旅游景区。" # Default description
        }

        # 1. Check if it exists in current attractions.json (preserve manual edits/good data)
        # However, checking the current file, it seems generated. 
        # But if we have valid coordinates there, we should keep them.
        if name in current_map:
            existing = current_map[name]
            if existing.get('lat') and existing.get('lng'):
                entry['lat'] = existing['lat']
                entry['lng'] = existing['lng']
                entry['location'] = existing.get('location', '')
                entry['description'] = existing.get('description', entry['description'])
                count_existing += 1
                final_list.append(entry)
                continue
        
        # 2. If not in current or no coords, look in CSV
        norm_name = normalize(name)
        csv_match = csv_exact_map.get(name) or csv_norm_map.get(norm_name)
        
        # Fuzzy match if strict failed
        match_type = "EXACT"
        if not csv_match:
            potential_matches = []
            for csv_name in csv_names:
                if csv_name in name or name in csv_name:
                    potential_matches.append(csv_name)
            if potential_matches:
                best_match = max(potential_matches, key=len)
                csv_match = poi_data[best_match]
                match_type = "PARTIAL"

        if csv_match:
            try:
                entry['lat'] = float(csv_match.get('POI_Latitude', 0))
                entry['lng'] = float(csv_match.get('POI_Longitude', 0))
                # Construct location string: Province City
                province = csv_match.get('一级行政区划(Adm1)', '')
                city = csv_match.get('二级行政区划(Adm2)', '')
                entry['location'] = f"{province} {city}".strip()
                entry['description'] = f"位于{province}{city}的国家5A级旅游景区。"
                
                if match_type == "EXACT":
                    count_csv_exact += 1
                else:
                    count_csv_partial += 1
            except ValueError:
                count_missing_loc += 1
        else:
            count_missing_loc += 1
            # print(f"Missing location for: {name}")

        final_list.append(entry)

    print("-" * 30)
    print(f"Total processed: {len(final_list)}")
    print(f"From existing JSON: {count_existing}")
    print(f"From CSV (Exact): {count_csv_exact}")
    print(f"From CSV (Partial): {count_csv_partial}")
    print(f"Missing coordinates: {count_missing_loc}")
    
    # Save to src/attractions.json
    with open('src/attractions.json', 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    print("Saved to src/attractions.json")

if __name__ == "__main__":
    main()
