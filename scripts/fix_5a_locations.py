import json
import csv
import re
from bs4 import BeautifulSoup

def normalize(name):
    # Remove references like [1]
    name = re.sub(r'\[.*?\]', '', str(name)).strip()
    # Normalize parentheses to full-width
    name = name.replace('(', '（').replace(')', '）')
    return name

def get_wiki_data():
    with open('scripts/raw_data/wiki_page.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_='wikitable')
    
    wiki_attractions = []
    
    for table in tables:
        rows = table.find_all('tr')
        if not rows: continue
        
        # Try to find headers to identify columns
        headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
        
        col_name = -1
        col_province = -1
        col_prefecture = -1
        col_county = -1
        
        for i, h in enumerate(headers):
            if '景区名称' in h or '名称' in h: col_name = i
            if '省级' in h: col_province = i
            if '地级' in h or '州市' in h: col_prefecture = i
            if '县级' in h or '县区' in h: col_county = i

        # Heuristic for cases where headers aren't standard or table is split
        if col_name == -1: col_name = 0
        
        # Track rowspan for province/prefecture
        rowspan_info = {} # col_index -> {"text": str, "remaining": int}

        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            if not cells: continue
            
            # Fill in data including rowspans
            row_data = {}
            cell_idx = 0
            
            num_cols = max(col_name, col_province, col_prefecture, col_county) + 1
            if num_cols < len(headers): num_cols = len(headers)

            for c_idx in range(num_cols):
                if c_idx in rowspan_info and rowspan_info[c_idx]["remaining"] > 0:
                    row_data[c_idx] = rowspan_info[c_idx]["text"]
                    rowspan_info[c_idx]["remaining"] -= 1
                elif cell_idx < len(cells):
                    cell = cells[cell_idx]
                    text = cell.get_text(strip=True)
                    row_data[c_idx] = text
                    
                    if cell.has_attr('rowspan'):
                        try:
                            span = int(cell['rowspan'])
                            if span > 1:
                                rowspan_info[c_idx] = {"text": text, "remaining": span - 1}
                        except ValueError:
                            pass
                    cell_idx += 1
                else:
                    row_data[c_idx] = ""

            name = normalize(row_data.get(col_name, ""))
            if not name or "名称" in name: continue
            
            wiki_attractions.append({
                "name": name,
                "province": normalize(row_data.get(col_province, "")),
                "prefecture": normalize(row_data.get(col_prefecture, "")),
                "county": normalize(row_data.get(col_county, ""))
            })
            
    return wiki_attractions

def fix_locations():
    print("Fetching Wikipedia data...")
    wiki_list = get_wiki_data()
    print(f"Extracted {len(wiki_list)} entries from Wikipedia.")
    
    # Process wiki_list to extract unit names from parentheses
    for w in wiki_list:
        m = re.search(r'（([^）]+)）$', w['name'])
        if m:
            w['unit_name'] = m.group(1)
        else:
            w['unit_name'] = w['name']
            
    print("Loading scenic_poi.csv...")
    poi_data = []
    with open('scripts/raw_data/scenic_poi.csv', 'r', encoding='utf-8') as f:
        f.readline()
        reader = csv.DictReader(f)
        for row in reader:
            poi_data.append(row)
    
    print("Loading current attractions.json...")
    with open('data/attractions.json', 'r', encoding='utf-8') as f:
        final_attractions = json.load(f)
        
    # Manual Overrides for 28 items missing in CSV or with suspicious coords (like Xi'an/Beijing defaults)
    manual_coords = {
        "九寨沟旅游景区": (33.083, 103.916),
        "六鼎山文化旅游区": (43.344, 128.197),
        "冶力关旅游区": (34.963, 103.659),
        "凤凰古城旅游区": (27.943, 109.604),
        "博斯腾湖景区": (41.95, 86.86),
        "和静巴音布鲁克景区": (42.798, 84.164),
        "喀拉峻景区": (43.0, 82.8),
        "塔克拉玛干·三五九旅文化旅游区": (36.33, 109.47),
        "大觉山景区": (27.695, 117.197),
        "恩施大峡谷景区": (30.465, 109.173),
        "新疆天山天池风景名胜区": (43.886, 88.132),
        "普者黑旅游景区": (24.115, 104.124),
        "槟榔谷黎苗文化旅游区": (18.399, 109.665),
        "汶川特别旅游区": (30.892, 103.376),
        "海螺沟景区": (29.567, 101.95),
        "炳灵寺世界文化遗产旅游区": (35.805, 103.044),
        "矮寨·十八洞·德夯大峡谷景区": (28.32, 109.58),
        "神农架生态旅游区": (31.744, 110.68),
        "神龙溪纤夫文化旅游区": (31.25, 110.05),
        "腾龙洞景区": (30.336, 108.983),
        "荔波樟江景区": (25.40, 107.96),
        "衡水湖旅游景区": (37.614, 115.591),
        "那拉提旅游风景区": (43.28, 84.22),
        "镇远古城旅游景区": (27.05, 108.42),
        "阿咪东索景区": (38.08, 100.22),
        "青海湖景区": (36.844, 100.190),
        "香格里拉普达措景区": (27.853, 100.019),
        "黄龙景区": (32.754, 103.822)
    }

    updated_count = 0
    mismatch_log = []
    
    for item in final_attractions:
        if item.get('category') and 'natgeo' in item.get('category'):
            continue
            
        name = item['name']
        
        # Priority: Manual Override
        if name in manual_coords:
            item['lat'], item['lng'] = manual_coords[name]
            updated_count += 1
            # Still need wiki_match for location standardization
        
        # Determine the target administrative info
        wiki_match = None
        # Try finding a direct match or a match by unit_name
        for w in wiki_list:
            if name == w['name'] or name == w['unit_name']:
                wiki_match = w
                break
        
        if not wiki_match:
            # Try fuzzy match against all names and unit_names
            for w in wiki_list:
                if name in w['name'] or w['name'] in name or name in w['unit_name'] or w['unit_name'] in name:
                    wiki_match = w
                    break
        
        if wiki_match:
            if name not in manual_coords:
                target_province = wiki_match['province'].replace('省', '').replace('市', '')
                # If it's a municipality, prefecture might be blank or the name itself
                target_prefecture = wiki_match['prefecture'].replace('市', '').replace('州', '').replace('地区', '')
                if not target_prefecture and target_province in ["北京", "天津", "上海", "重庆"]:
                    target_prefecture = target_province
                
                target_county = wiki_match['county'].replace('区', '').replace('县', '').replace('市', '')
                
                # Now find the best coordinate in POI data
                best_poi = None
                
                # Use keywords for better fuzzy name matching in CSV
                # Rank 1: Both name and province match
                # Rank 2: Only name matches AND it's a unique match
                # Rank 3: Part of name matches AND province matches
                
                # Use a scoring system
                matches_with_scores = []
                
                # Clean targets for matching
                def clean_region(n):
                    for s in ["自治区", "回族", "维吾尔", "壮族", "藏族", "省", "市", "区", "县"]:
                        n = n.replace(s, "")
                    return n

                clean_prov = clean_region(target_province)
                clean_pref = clean_region(target_prefecture) if target_prefecture else ""

                for poi in poi_data:
                    poi_name = poi['景区名称']
                    poi_prov = poi['一级行政区划(Adm1)']
                    poi_pref = poi['二级行政区划(Adm2)']
                    
                    score = 0
                    if name == poi_name: score += 100
                    elif name in poi_name or poi_name in name: score += 50
                    
                    if clean_prov in poi_prov: score += 200
                    if clean_pref and clean_pref in poi_pref: score += 150
                    
                    if score > 200: 
                        matches_with_scores.append((score, poi))
                
                if matches_with_scores:
                    matches_with_scores.sort(key=lambda x: x[0], reverse=True)
                    best_poi = matches_with_scores[0][1]
                    item['lat'] = float(best_poi['POI_Latitude'])
                    item['lng'] = float(best_poi['POI_Longitude'])
                    updated_count += 1
                else:
                    if not item.get('lat') or not item.get('lng'):
                        mismatch_log.append(f"STILL MISSING COORDS: {name}")
            
            # ALWAYS update location and description from Wiki data for consistency
            item['location'] = f"{wiki_match['province']} {wiki_match['prefecture']} {wiki_match['county']}".strip()
            item['description'] = f"位于{wiki_match['province']}{wiki_match['prefecture']}{wiki_match['county']}的国家5A级旅游景区。"
        else:
            mismatch_log.append(f"No Wiki match found for: {name}")

    print(f"Total synced: {len(final_attractions)-len([x for x in final_attractions if 'natgeo' in x.get('category','')])-len(mismatch_log)} / 359")
    for log in sorted(mismatch_log): print(log)
    print("Standardized all 5A locations and descriptions based on Wikipedia.")

    for log in sorted(mismatch_log):
        print(log)

    
    with open('data/attractions.json', 'w', encoding='utf-8') as f:
        json.dump(final_attractions, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    fix_locations()
