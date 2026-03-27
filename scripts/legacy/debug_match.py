from scripts.merge_data import load_poi_data, normalize_name, find_best_match

def test_match():
    print("Loading valid POI data...")
    poi_map = load_poi_data('data/scenic_poi.csv')
    
    target = "乐山市峨眉山景区"
    print(f"\nTarget: {target}")
    print(f"Normalized Target: {normalize_name(target)}")
    
    # Check if '峨眉山' related entries exist in POI map
    print("\nSearching POI map for '峨眉':")
    found = False
    for name in poi_map:
        if '峨眉' in name:
            found = True
            norm = normalize_name(name)
            print(f"POI: '{name}' -> Normalized: '{norm}'")
            if norm in normalize_name(target):
                print(f"   MATCH FOUND via substring: '{norm}' in '{normalize_name(target)}'")
            
    if not found:
        print("No POI found with '峨眉'")

    # Run actual match
    match = find_best_match(target, poi_map)
    print(f"\nResult of find_best_match: {match is not None}")

if __name__ == "__main__":
    test_match()
