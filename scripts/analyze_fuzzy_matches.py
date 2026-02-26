import json
import csv
import difflib

def analyze_matches():
    json_path = 'src/attractions.json'
    csv_path = 'scenic_poi.csv'
    
    # Load JSON data - get missing names
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            attractions = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_path} not found.")
        return

    missing_names = []
    for item in attractions:
        if item.get('lat') is None or item.get('lng') is None:
            missing_names.append(item['name'])

    # Load CSV data - get all names
    csv_names = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) 
            next(reader)
            for row in reader:
                if len(row) >= 5:
                    name = row[2]
                    try:
                        lat = float(row[3])
                        lng = float(row[4])
                        csv_names[name] = {'lat': lat, 'lng': lng}
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
        return

    csv_name_list = list(csv_names.keys())
    
    # Find matches
    print(f"Analyzing {len(missing_names)} missing items against {len(csv_name_list)} CSV items...\n")
    
    matched_count = 0
    
    for missing in missing_names:
        # 1. Exact match
        if missing in csv_names:
            print(f"[EXACT] {missing}")
            matched_count += 1
            continue
            
        # 2. Contains match (either way)
        contains_matches = [n for n in csv_name_list if missing in n or n in missing]
        if contains_matches:
             # Pick the longest match? or just the first
             print(f"[CONTAIN] {missing} -> {contains_matches[0]}")
             matched_count += 1
             continue
             
        # 3. Fuzzy match
        matches = difflib.get_close_matches(missing, csv_name_list, n=1, cutoff=0.5)
        if matches:
            print(f"[FUZZY]   {missing} -> {matches[0]}")
            matched_count += 1
        else:
            print(f"[NONE]    {missing}")

    print(f"\nTotal potentially matched: {matched_count}/{len(missing_names)}")

if __name__ == "__main__":
    analyze_matches()
