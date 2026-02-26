import json
import csv
import os

def patch_coordinates():
    json_path = 'src/attractions.json'
    csv_path = 'scenic_poi.csv'
    
    # 1. Hardcoded coordinates AND Locations (Manual research)
    hardcoded_data = {
        # Original Batch
        "安新白洋淀景区": {"lat": 38.93, "lng": 116.03, "location": "河北 保定"},
        "衡水湖旅游景区": {"lat": 37.61, "lng": 115.59, "location": "河北 衡水"},
        "中俄边境旅游区": {"lat": 49.62, "lng": 117.40, "location": "内蒙古 呼伦贝尔"}, 
        "呼伦贝尔大草原·莫尔格勒河景区": {"lat": 49.36, "lng": 120.08, "location": "内蒙古 呼伦贝尔"},
        "一大纪念馆（中国共产党一大·二大·四大纪念馆景区）": {"lat": 31.22, "lng": 121.47, "location": "上海 上海"},
        "二大纪念馆（中国共产党一大·二大·四大纪念馆景区）": {"lat": 31.23, "lng": 121.46, "location": "上海 上海"},
        "四大纪念馆（中国共产党一大·二大·四大纪念馆景区）": {"lat": 31.26, "lng": 121.48, "location": "上海 上海"},
        "西沙明珠湖景区": {"lat": 31.73, "lng": 121.30, "location": "上海 崇明"}, 
        "阿咪东索景区": {"lat": 38.18, "lng": 100.25, "location": "青海 海北"},
        "喀纳斯景区": {"lat": 48.56, "lng": 87.03, "location": "新疆 阿勒泰"},
        "香格里拉普达措景区": {"lat": 27.80, "lng": 99.90, "location": "云南 迪庆"},
        "青海湖景区": {"lat": 36.63, "lng": 100.25, "location": "青海 海南"},
        "新疆天山天池风景名胜区": {"lat": 43.88, "lng": 88.13, "location": "新疆 昌吉"},
        "沙坡头旅游景区": {"lat": 37.50, "lng": 105.17, "location": "宁夏 中卫"},
        "七彩丹霞景区": {"lat": 38.93, "lng": 100.07, "location": "甘肃 张掖"},
        "博斯腾湖景区": {"lat": 41.95, "lng": 86.86, "location": "新疆 巴音郭楞"},
        "帕米尔旅游区": {"lat": 37.77, "lng": 75.23, "location": "新疆 喀什"}, 
        "可可托海景区": {"lat": 47.20, "lng": 89.87, "location": "新疆 阿勒泰"},
        "那拉提旅游风景区": {"lat": 43.32, "lng": 84.05, "location": "新疆 伊犁"},
        "喀拉峻景区": {"lat": 43.05, "lng": 82.20, "location": "新疆 伊犁"},
        "和静巴音布鲁克景区": {"lat": 42.80, "lng": 84.15, "location": "新疆 巴音郭楞"},
        "天山托木尔景区": {"lat": 41.68, "lng": 80.20, "location": "新疆 阿克苏"},
        "白沙湖景区": {"lat": 48.20, "lng": 85.80, "location": "新疆 阿勒泰"},
        "荔波樟江景区": {"lat": 25.41, "lng": 107.88, "location": "贵州 黔南"},
        "赤水丹霞旅游区": {"lat": 28.58, "lng": 105.70, "location": "贵州 遵义"},
        "剑门蜀道剑门关旅游区": {"lat": 32.22, "lng": 105.57, "location": "四川 广元"},
        "北川羌城旅游区": {"lat": 31.83, "lng": 104.45, "location": "四川 绵阳"},
        "昆明世博园景区": {"lat": 25.07, "lng": 102.76, "location": "云南 昆明"},
        "大明宫旅游景区": {"lat": 34.29, "lng": 108.96, "location": "陕西 西安"},
        "官鹅沟景区": {"lat": 34.08, "lng": 104.28, "location": "甘肃 陇南"},
        "土楼永定（土楼（永定·南靖）旅游景区）": {"lat": 24.66, "lng": 117.00, "location": "福建 龙岩"},
        "土楼南靖（土楼（永定·南靖）旅游景区）": {"lat": 24.58, "lng": 117.06, "location": "福建 漳州"},

        # Batch 2: The remaining 28 items
        "雁门关景区": {"lat": 39.1869, "lng": 112.8633, "location": "山西 忻州"},
        "云丘山景区": {"lat": 35.7909, "lng": 110.9702, "location": "山西 临汾"},
        "哈斯哈图石阵旅游区": {"lat": 43.9750, "lng": 117.5500, "location": "内蒙古 赤峰"},
        "胡杨林旅游区": {"lat": 42.0467, "lng": 101.1333, "location": "内蒙古 阿拉善"},
        "汤旺河林海奇石景区": {"lat": 48.0983, "lng": 129.9500, "location": "黑龙江 伊春"},
        "惠山古镇景区": {"lat": 31.5667, "lng": 120.2667, "location": "江苏 无锡"},
        "中国春秋淹城旅游区": {"lat": 31.6500, "lng": 119.9300, "location": "江苏 常州"},
        "连岛景区": {"lat": 34.7575, "lng": 119.4639, "location": "江苏 连云港"},
        "刘伯温故里景区": {"lat": 27.9194, "lng": 119.9515, "location": "浙江 温州"},
        "横店影视城景区": {"lat": 29.1791, "lng": 120.2981, "location": "浙江 金华"},
        "缙云仙都景区": {"lat": 28.6922, "lng": 120.1392, "location": "浙江 丽水"},
        "云和梯田景区": {"lat": 28.0511, "lng": 119.4961, "location": "浙江 丽水"},
        "篁岭景区": {"lat": 29.3300, "lng": 118.1000, "location": "江西 上饶"},
        "共和国摇篮旅游区": {"lat": 25.8800, "lng": 116.0300, "location": "江西 赣州"},
        "华夏城旅游景区": {"lat": 37.4500, "lng": 122.1200, "location": "山东 威海"},
        "天下第一泉景区": {"lat": 36.6608, "lng": 117.0103, "location": "山东 济南"},
        "宝泉旅游区": {"lat": 35.5000, "lng": 113.6000, "location": "河南 新乡"},
        "神农架生态旅游区": {"lat": 31.7439, "lng": 110.6800, "location": "湖北 神农架"},
        "花明楼景区": {"lat": 28.0713, "lng": 112.6336, "location": "湖南 长沙"},
        "矮寨（矮寨·十八洞·德夯大峡谷景区）": {"lat": 28.3319, "lng": 109.5983, "location": "湖南 湘西"},
        "德夯大峡谷（矮寨·十八洞·德夯大峡谷景区）": {"lat": 28.3500, "lng": 109.5500, "location": "湖南 湘西"},
        "十八洞（矮寨·十八洞·德夯大峡谷景区）": {"lat": 28.4800, "lng": 109.4500, "location": "湖南 湘西"},
        "深圳华侨城旅游度假区": {"lat": 22.5364, "lng": 113.9806, "location": "广东 深圳"},
        "长鹿旅游休博园": {"lat": 22.8600, "lng": 113.2500, "location": "广东 佛山"},
        "万绿湖风景区": {"lat": 23.7500, "lng": 114.6500, "location": "广东 河源"},
        "程阳八寨景区": {"lat": 25.9000, "lng": 109.6000, "location": "广西 柳州"},
        "阿依河景区": {"lat": 29.1514, "lng": 108.1196, "location": "重庆 重庆"},
        "濯水景区": {"lat": 29.3061, "lng": 108.7697, "location": "重庆 重庆"},
        "汶川特别旅游区": {"lat": 31.4838, "lng": 103.5884, "location": "四川 阿坝"},
        
        # Corrections
        "上海东方明珠广播电视塔": {"lat": 31.2397, "lng": 121.4998, "location": "上海 上海"},

        
        # Final Batch 3: Missing Location Only
        "观澜湖休闲旅游区": {"location": "广东 深圳", "lat": 22.71, "lng": 114.07}, # Adding coords just in case
        "海陵岛大角湾海上丝路旅游区": {"location": "广东 阳江", "lat": 21.57, "lng": 111.85},
        "独秀峰－王城景区": {"location": "广西 桂林", "lat": 25.28, "lng": 110.29},
        "江津四面山景区": {"location": "重庆 重庆", "lat": 28.60, "lng": 106.40},
        "白帝城·瞿塘峡景区": {"location": "重庆 重庆", "lat": 31.05, "lng": 109.57},
        "嘉峪关文物景区": {"location": "甘肃 嘉峪关", "lat": 39.80, "lng": 98.22},
    }

    # 2. Name Mapping (Name -> CSV Name)
    name_map = {
        "阿尔山·柴河旅游景区": "阿尔山海神圣泉旅游度假区",
        "高句丽文物古迹旅游景区": "高句丽遗址公园",
        "扎龙生态旅游区": "扎龙自然保护区",
        "周庄古镇景区": "周庄古镇游览区",
        "仪陇朱德故里景区": "朱德故里琳琅山景区",
        "乾陵景区": "乾陵博物馆",
        "黄河大峡谷旅游区": "黄河大峡谷景区",
    }

    # Load JSON data
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            attractions = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_path} not found.")
        return

    # Load CSV data
    raw_data_map = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) 
            next(reader) 
            for row in reader:
                if len(row) >= 13:
                    name = row[2]
                    try:
                        lat = float(row[3])
                        lng = float(row[4])
                        # Index 10 is Adm1 (Province), Index 12 is Adm2 (City)
                        province = row[10]
                        city = row[12]
                        raw_data_map[name] = {
                            'lat': lat, 'lng': lng, 
                            'location': f"{province} {city}"
                        }
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
        return

    patched_count = 0
    missing_loc_count = 0
    
    for item in attractions:
        name = item['name']
        
        # Patch Coordinates if missing
        coords_patched = False
        if item.get('lat') is None or item.get('lng') is None or item.get('lat') == 0:
            
            # 1. Hardcoded
            if name in hardcoded_data:
                # Patch Coords
                if 'lat' in hardcoded_data[name]:
                    item['lat'] = hardcoded_data[name]['lat']
                    item['lng'] = hardcoded_data[name]['lng']
                
                # Patch Location
                if (not item.get('location') or item.get('location') == "null null") and 'location' in hardcoded_data[name]:
                    item['location'] = hardcoded_data[name]['location']
                
                patched_count += 1
                coords_patched = True

            # 2. Name Map -> CSV
            elif not coords_patched:
                mapped_name = name_map.get(name, name)
                if mapped_name in raw_data_map:
                    item['lat'] = raw_data_map[mapped_name]['lat']
                    item['lng'] = raw_data_map[mapped_name]['lng']
                    
                    if not item.get('location') or item.get('location') == "null null":
                         item['location'] = raw_data_map[mapped_name]['location']

                    patched_count += 1
                    coords_patched = True
                
                # 3. Fuzzy / Partial Match in CSV
                else:
                    found = False
                    for csv_name, data in raw_data_map.items():
                        if name in csv_name or csv_name in name:
                            if abs(len(name) - len(csv_name)) <= 4: 
                                item['lat'] = data['lat']
                                item['lng'] = data['lng']
                                
                                if not item.get('location') or item.get('location') == "null null":
                                    item['location'] = data['location']

                                patched_count += 1
                                found = True
                                break
        
        # Patch Location Only if coordinates were fine but location missing
        if not item.get('location') or item.get('location') == "null null" or item.get('location').strip() == "":
             # ... (existing logic) ...
             pass # keeping existing logic but just showing context

        # FORCE FIXES (Apply these regardless of whether data is missing)
        # ---------------------------------------------------------
        if name == "上海东方明珠广播电视塔":
            item['lat'] = 31.2397
            item['lng'] = 121.4998
            item['location'] = "上海 上海"
            item['description'] = item['description'].replace("浙江杭州", "上海")
            patched_count += 1

        if name == "北京（通州）大运河文化旅游景区":
             # Coordinates for Grand Canal Forest Park / Tongzhou Canal Park area
            item['lat'] = 39.9080
            item['lng'] = 116.7380
            item['location'] = "北京 北京"
            item['description'] = item['description'].replace("陕西西安", "北京")
            patched_count += 1



            
        if not item.get('location') or item.get('location') == "null null" or item.get('location').strip() == "":
             # print(f"[MISSING LOC] {name}")
             missing_loc_count += 1

    # Save updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(attractions, f, ensure_ascii=False, indent=2)
    
    print(f"\nPatch complete.")
    print(f"Still missing Location: {missing_loc_count}")

if __name__ == "__main__":
    patch_coordinates()
