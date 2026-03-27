import json

def check_locations():
    json_path = 'src/attractions.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            attractions = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_path} not found.")
        return

    missing_count = 0
    print("Items with missing location:")
    for item in attractions:
        loc = item.get('location')
        if not loc or loc.strip() == "" or loc == "null null": # Check for various "empty" states
            print(f"- {item['name']} (ID: {item['id']})")
            missing_count += 1
            
    print(f"\nTotal missing location: {missing_count}")

if __name__ == "__main__":
    check_locations()
