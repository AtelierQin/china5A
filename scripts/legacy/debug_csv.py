with open('data/scenic_poi.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"Line 0 repr: {repr(lines[0])}")
    print(f"Line 1 repr: {repr(lines[1])}")
