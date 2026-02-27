import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import ssl

def get_baike_image(term):
    url = f"https://baike.baidu.com/item/{urllib.parse.quote(term)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    context = ssl._create_unverified_context()
    try:
        html = urllib.request.urlopen(req, context=context, timeout=10).read()
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.select_one('.summary-pic img')
        if img and img.has_attr('src'):
            return img['src']
    except Exception as e:
        print(f"Error {term}: {e}")
    return None

print(get_baike_image("八达岭长城"))
