import urllib.request
import urllib.parse
import json
import ssl

WIKI_API_URL = "https://zh.wikipedia.org/w/api.php"
USER_AGENT = 'China5AExplorer/1.0'

def search_wiki(term):
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": term,
        "utf8": 1,
        "srlimit": 1
    }
    query_string = urllib.parse.urlencode(params)
    url = f"{WIKI_API_URL}?{query_string}"
    
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    context = ssl._create_unverified_context()
    try:
        html = urllib.request.urlopen(req, context=context, timeout=10).read()
        data = json.loads(html.decode())
        search_results = data.get("query", {}).get("search", [])
        if search_results:
            return search_results[0]["title"]
    except Exception as e:
        print(f"Error {term}: {e}")
    return None

def get_wiki_image(title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": title,
        "pithumbsize": 800
    }
    
    query_string = urllib.parse.urlencode(params)
    url = f"{WIKI_API_URL}?{query_string}"
    
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    context = ssl._create_unverified_context()
    try:
        html = urllib.request.urlopen(req, context=context, timeout=10).read()
        data = json.loads(html.decode())
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if "thumbnail" in page_data:
                return page_data["thumbnail"]["source"]
    except Exception as e:
        print(f"Error {title}: {e}")
    return None

test_cases = ["八达岭长城（八达岭-慕田峪长城）", "奥林匹克公园", "天津古文化街旅游区（津门故里）", "衡水湖旅游景区"]
for name in test_cases:
    print(f"Testing: {name}")
    title = search_wiki(name)
    print(f"  Found title: {title}")
    if title:
        img = get_wiki_image(title)
        print(f"  Found image: {img}")
    print()
