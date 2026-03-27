import urllib.request
import urllib.parse
import json
import ssl
import time
import re
import os

# Constants
INPUT_FILE = 'src/attractions.json'
OUTPUT_FILE = 'src/attractions.json'
WIKI_API_URL = "https://zh.wikipedia.org/w/api.php"
COMMONS_API_URL = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = 'China5AExplorer/1.0 (https://github.com/yourusername/china5a; contact@example.com)'

def clean_name(name):
    """
    Remove common suffixes to increase search hit rate.
    """
    # Remove content inside parenthesis
    name = re.sub(r'（.*?）', '', name)
    name = re.sub(r'\(.*?\)', '', name)
    
    # Remove common suffixes
    suffixes = [
        "旅游景区", "风景名胜区", "旅游区", "景区", "风景区", 
        "文化旅游区", "生态旅游区", "遗址公园", "博物馆", "纪念馆",
        "公园", "故里"
    ]
    
    # Sort suffixes by length (descending) to match longest first
    suffixes.sort(key=len, reverse=True)
    
    cleaned = name
    for suffix in suffixes:
        if cleaned.endswith(suffix):
            cleaned = cleaned[:-len(suffix)]
            break
            
    return cleaned.strip()

def search_commons_image(term):
    """Search for files in Wikimedia Commons"""
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": f"filetype:bitmap {term}",
        "srnamespace": 6, # File namespace
        "utf8": 1,
        "srlimit": 1
    }
    query_string = urllib.parse.urlencode(params)
    url = f"{COMMONS_API_URL}?{query_string}"
    
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    context = ssl._create_unverified_context()
    try:
        html = urllib.request.urlopen(req, context=context, timeout=10).read()
        data = json.loads(html.decode())
        search_results = data.get("query", {}).get("search", [])
        if search_results:
            title = search_results[0]["title"]
            return get_commons_image_url(title)
    except Exception as e:
        print(f"Error Commons Search {term}: {e}")
    return None

def get_commons_image_url(title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": 800,
        "titles": title
    }
    query_string = urllib.parse.urlencode(params)
    url = f"{COMMONS_API_URL}?{query_string}"
    
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    context = ssl._create_unverified_context()
    try:
        html = urllib.request.urlopen(req, context=context, timeout=10).read()
        data = json.loads(html.decode())
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if "imageinfo" in page_data and len(page_data["imageinfo"]) > 0:
                info = page_data["imageinfo"][0]
                return info.get("thumburl", info.get("url"))
    except Exception as e:
        print(f"Error Commons URL {title}: {e}")
    return None

def get_wiki_image(term, original_name=None):
    """
    Fetch image URL from Wikipedia given a search term.
    """
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": term,
        "pithumbsize": 800  # Request a reasonably large thumbnail
    }
    
    query_string = urllib.parse.urlencode(params)
    url = f"{WIKI_API_URL}?{query_string}"
    
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    
    try:
        # Create a context that doesn't verify SSL certificates
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            data = json.loads(response.read().decode())
            pages = data.get("query", {}).get("pages", {})
            
            # Check for -1 (missing)
            if "-1" in pages:
                # If term fails, try with original full name if different
                if original_name and original_name != term:
                     return get_wiki_image(original_name)
                return None
            
            for page_id, page_data in pages.items():
                if "thumbnail" in page_data:
                    return page_data["thumbnail"]["source"]
    except Exception as e:
        print(f"Error fetching {term}: {e}")
        return None
    
    return None

def main():
    print(f"Reading from {INPUT_FILE}...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        attractions = json.load(f)
    
    updated_count = 0
    total = len(attractions)
    
    print(f"Found {total} attractions. Starting image fetch...")
    
    for i, attraction in enumerate(attractions):
        current_image = attraction.get('image', '')
        
        # Skip if already has a real image (checking for non-placeholder)
        if current_image and "placehold.co" not in current_image and "wikimedia" in current_image:
             print(f"[{i+1}/{total}] Skipping {attraction['name']} (Already has image)")
             continue
             
        name = attraction['name']
        cleaned_name = clean_name(name)
        
        # Try fetching with cleaned name first, fallback to original inside function
        print(f"[{i+1}/{total}] Fetching for '{name}' (Search: '{cleaned_name}')...")
        
        image_url = get_wiki_image(cleaned_name, original_name=name)
        
        # Fallback to Commons API search
        if not image_url:
             print(f"  -> Wiki article image failed, searching Commons...")
             # Search Commons using cleaned name
             image_url = search_commons_image(cleaned_name)
             if not image_url and cleaned_name != name:
                 # Try with original full name
                 image_url = search_commons_image(name)

        if image_url:
            attraction['image'] = image_url
            updated_count += 1
            print(f"  -> Found: {image_url}")
        else:
            print(f"  -> No image found.")
            
        # Be nice to the API
        time.sleep(0.1)
        
        # Save periodically
        if (i + 1) % 10 == 0:
             with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(attractions, f, ensure_ascii=False, indent=2)

    # Final save
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(attractions, f, ensure_ascii=False, indent=2)
        
    print(f"Done! Updated {updated_count} attractions.")

if __name__ == "__main__":
    main()
