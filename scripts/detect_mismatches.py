import json

def get_prov(name):
    provs = ["北京","天津","河北","山西","内蒙古","辽宁","吉林","黑龙江","上海","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","广西","海南","重庆","四川","贵州","云南","西藏","陕西","甘肃","青海","宁夏","新疆"]
    for p in provs:
        if p in name: return p
    return None

def main():
    with open('data/attractions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    mismatches = []
    
    # Specific known cities linking to province
    city_to_prov = {
        "张家界": "湖南",
        "苏州": "江苏",
        "杭州": "浙江",
        "成都": "四川",
        "西安": "陕西",
        "广州": "广东",
        "深圳": "广东",
        "武汉": "湖北",
        "南京": "江苏",
        "青岛": "山东",
        "黄山": "安徽",
        "丽江": "云南",
        "桂林": "广西"
    }

    for item in data:
        if item.get('category') and 'natgeo' in item.get('category'): continue
        
        name = item['name']
        loc = item.get('location', '')
        
        expected_prov = get_prov(name)
        if not expected_prov:
            for city, p in city_to_prov.items():
                if city in name:
                    expected_prov = p
                    break
                    
        if expected_prov:
            # check if expected_prov is in loc
            if expected_prov not in loc:
                mismatches.append(f"[{name}] assigned to '{loc}', expected '{expected_prov}'")
                
    for m in mismatches:
        print(m)

if __name__ == "__main__":
    main()
