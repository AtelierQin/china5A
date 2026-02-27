import urllib.request
import urllib.parse
import json
import ssl

COMMONS_API_URL = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = 'China5AExplorer/1.0'

def search_commons_image(term):
    # Search for files in Wikimedia Commons
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
            # Now get the actual image URL
            return get_commons_image_url(title)
    except Exception as e:
        print(f"Error {term}: {e}")
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
        print(f"Error URL {title}: {e}")
    return None

test_cases = ["八达岭长城", "奥林匹克公园", "天津古文化街", "衡水湖", "白石山", "广府古城"]
for name in test_cases:
    print(f"Testing Commons: {name}")
    img = search_commons_image(name)
    print(f"  Found image: {img}\n")

