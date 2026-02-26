import urllib.request
import urllib.parse
import json
import ssl

def get_wiki_image(term):
    base_url = "https://zh.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": term,
        "pithumbsize": 600
    }
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_string}"
    
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'China5AExplorer/1.0 (https://github.com/example/china5a; contact@example.com)')
    
    try:
        # Create a context that doesn't verify SSL certificates (for development/testing)
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            data = json.loads(response.read().decode())
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if "thumbnail" in page_data:
                    return page_data["thumbnail"]["source"]
    except Exception as e:
        print(f"Error fetching {term}: {e}")
    return None

def main():
    term = "故宫博物院"
    print(f"Fetching image for {term}...")
    img_url = get_wiki_image(term)
    print(f"Image for {term}: {img_url}")
    
    term2 = "天坛公园"
    print(f"Fetching image for {term2}...")
    img_url2 = get_wiki_image(term2)
    print(f"Image for {term2}: {img_url2}")

if __name__ == "__main__":
    main()
