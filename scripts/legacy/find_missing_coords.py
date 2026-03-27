import json

def find_missing_coords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    missing_list = []
    for item in data:
        if item.get('lat') is None or item.get('lng') is None:
            missing_list.append(item['name'])
    
    return missing_list

if __name__ == "__main__":
    missing = find_missing_coords('src/attractions.json')
    
    with open('docs/missing_coordinates.md', 'w', encoding='utf-8') as f:
        f.write("# 缺失坐标系的国家5A级旅游景区\n\n")
        f.write(f"共发现 {len(missing)} 个景区缺失坐标信息：\n\n")
        for name in missing:
            f.write(f"- {name}\n")
            
    print(f"Report generated at docs/missing_coordinates.md with {len(missing)} items.")
