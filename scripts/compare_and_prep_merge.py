import json
import csv
import re

def normalize(name):
    """Normalize name for easier matching."""
    return re.sub(r'[（\(].*?[）\)]', '', name).strip()

def load_json(filepath):
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
    # Load attributes
    current_data = load_json('src/attractions.json')
    wiki_list = load_json('data/wiki_attractions.json')
    poi_data = load_csv('data/scenic_poi.csv')

    current_names = {item['name'] for item in current_data}
    
    # Wiki list is a list of strings
    missing_names = [name for name in wiki_list if name not in current_names]
    
    print(f"Total current: {len(current_names)}")
    print(f"Total wiki: {len(wiki_list)}")
    print(f"Missing count: {len(missing_names)}")

    # Check match in CSV
    found_in_csv = 0
    missing_in_csv = []
    
    csv_norm_map = {normalize(k): v for k, v in poi_data.items()}
    csv_names = list(poi_data.keys())

    print("\n--- Missing Items Analysis ---")
    for name in missing_names:
        norm_name = normalize(name)
        match = poi_data.get(name) or csv_norm_map.get(norm_name)
        
        if not match:
            # Partial match
            potential_matches = []
            for csv_name in csv_names:
                if csv_name in name or name in csv_name:
                    potential_matches.append(csv_name)
            
            if potential_matches:
                best_match = max(potential_matches, key=len)
                match = poi_data[best_match]
                # print(f"[PARTIAL] {name} -> {best_match}")

        if match:
            found_in_csv += 1
        else:
            missing_in_csv.append(name)
            print(f"[MISSING LOC] {name}")

    print(f"\nFound coordinates for {found_in_csv} of {len(missing_names)} missing items.")
    print(f"Still need coordinates for {len(missing_in_csv)} items.")

if __name__ == "__main__":
    main()
