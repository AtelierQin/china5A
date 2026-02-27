import json
import re

def normalize_name(name):
    """Normalize attraction name for comparison."""
    # Remove citations like [1]
    name = re.sub(r'\[\d+\]', '', name)
    # Normalize parentheses to full-width
    name = name.replace('(', '（').replace(')', '）')
    # Remove hidden texts or extra tags if any remain
    name = re.sub(r'<[^>]+>', '', name)
    # Remove spaces
    name = name.replace(' ', '')
    return name.strip()

def load_names(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list):
        # Handle list of dicts (data_5a.json) or list of strings (wiki.json)
        if data and isinstance(data[0], dict):
            return {normalize_name(item['name']): item['name'] for item in data}
        else:
            return {normalize_name(item): item for item in data}
    return set()

def main():
    local_data = load_names('data/data_5a.json')
    wiki_data = load_names('data/wiki_attractions.json')
    
    local_names = set(local_data.keys())
    wiki_names = set(wiki_data.keys())
    
    print(f"Local count: {len(local_names)}")
    print(f"Wiki count: {len(wiki_names)}")
    
    missing_in_local_keys = wiki_names - local_names
    extra_in_local_keys = local_names - wiki_names
    
    missing_in_local = [wiki_data[k] for k in missing_in_local_keys]
    extra_in_local = [local_data[k] for k in extra_in_local_keys]
    
    if missing_in_local:
        print("\nMissing in local dataset (Actually missing):")
        for name in sorted(missing_in_local):
            print(f"- {name}")
            
    if extra_in_local:
        print("\nExtra in local dataset (Possibly names or delisted):")
        for name in sorted(extra_in_local):
            print(f"- {name}")

    if not missing_in_local and not extra_in_local:
        print("\nSuccess: Both lists are identical!")

if __name__ == "__main__":
    main()
