import json
import re
from html.parser import HTMLParser

def normalize_name(name):
    """Normalize attraction name for comparison."""
    # Remove citations like [1]
    name = re.sub(r'\[\d+\]', '', name)
    # Normalize parentheses to full-width
    name = name.replace('(', '（').replace(')', '）')
    # Remove hidden texts or extra tags if any remain
    # (HTMLParser handles entities, but let's be safe)
    return name.strip()

def load_local_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {normalize_name(item['name']) for item in data}
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return set()

class WikiTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = []
        self.current_row = []
        self.in_cell = False
        self.cell_data = []
        self.is_wikitable = False
        self.row_idx = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            # Check class for 'wikitable'
            classes = [v for k, v in attrs if k == 'class']
            if classes and 'wikitable' in classes[0]:
                self.is_wikitable = True
                self.current_table = []
                self.row_idx = 0
        
        if self.is_wikitable and tag == 'tr':
            self.current_row = []

        if self.is_wikitable and tag in ['td', 'th']:
            self.in_cell = True
            # Store attrs to check for rowspan later if needed, 
            # but simple parser here usually just grabs text.
            # We'll just grab text for now.
            # Ideally we'd parse attributes for rowspan but HTMLParser SAX style makes it tricky 
            # to associate with the current cell data buffer.
            # Let's just grab the attributes here if we need them.
            # For this simple script, we'll try to survive without rowspan logic first
            # by detecting "Name" column index.
            self.current_attrs = dict(attrs)
            self.cell_data = []

    def handle_endtag(self, tag):
        if tag == 'table':
            if self.is_wikitable:
                self.tables.append(self.current_table)
                self.is_wikitable = False
        
        if self.is_wikitable and tag == 'tr':
            if self.current_row:
                self.current_table.append(self.current_row)
                self.row_idx += 1
        
        if self.is_wikitable and tag in ['td', 'th']:
            self.in_cell = False
            text = ''.join(self.cell_data).strip()
            # We could store (text, rowspan) tuple if we wanted to handle rowspan
            rowspan = int(self.current_attrs.get('rowspan', 1)) 
            self.current_row.append({'text': text, 'rowspan': rowspan})

    def handle_data(self, data):
        if self.in_cell:
            self.cell_data.append(data)

def load_wiki_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = WikiTableParser()
    parser.feed(content)
    
    all_names = set()
    
    for table in parser.tables:
        if not table: continue
        # Find header row
        headers = [c['text'] for c in table[0]]
        
        name_idx = -1
        for i, h in enumerate(headers):
            if '景点名称' in h:
                name_idx = i
                break
        
        if name_idx == -1: continue
        
        # Build a grid to handle rowspan
        num_rows = len(table)
        num_cols = len(headers) # assume header defines width
        
        # Create grid filled with None
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        
        # Fill grid
        # We need to track current position in each row
        # But this is tricky because `table` list only contains the *defined* cells for each row.
        # We process row by row, keeping track of "occupied" cells from previous rowspans.
        
        matrix = [[None for _ in range(num_cols)] for _ in range(num_rows)]
        
        for r_idx, row in enumerate(table):
            if r_idx == 0: continue # skip header
            
            c_idx = 0 # matrix column index
            cell_idx = 0 # source row cell list index
            
            while c_idx < num_cols:
                # If this spot is taken by a previous rowspan, skip it
                if matrix[r_idx][c_idx] is not None:
                    c_idx += 1
                    continue
                
                # Check if we have more cells in the source row
                if cell_idx < len(row):
                    cell = row[cell_idx]
                    text = cell['text']
                    rowspan = cell['rowspan']
                    # We assume colspan=1 for simplicity here as it's rare for name column
                    
                    # Fill current and future slots
                    for i in range(rowspan):
                        if r_idx + i < num_rows:
                            matrix[r_idx + i][c_idx] = text
                    
                    cell_idx += 1
                    c_idx += 1
                else:
                    break
        
        # Now extract data from the name column
        for r_idx in range(1, num_rows):
            if name_idx < len(matrix[r_idx]):
                name = matrix[r_idx][name_idx]
                if name:
                    # Clean up
                    name = normalize_name(name)
                    # Filter out delisted (usually we can't see 'del' tag here but text remains)
                    # Heuristic: verify if it matches local data logic
                    if name:
                        all_names.add(name)

    return all_names

def main():
    local_names = load_local_data('data_5a.json')
    try:
        wiki_names = load_wiki_data('wiki_content.html')
    except Exception as e:
        import traceback
        traceback.print_exc()
        return

    print(f"Local count: {len(local_names)}")
    print(f"Wiki count: {len(wiki_names)}")
    
    missing_in_local = wiki_names - local_names
    extra_in_local = local_names - wiki_names
    
    # Filter out potential mostly-matching names using simple similarity not implemented here,
    # but let's list them first.
    
    if missing_in_local:
        print("\nMissing in local dataset (or name mismatch):")
        for name in sorted(missing_in_local):
            print(f"- {name}")
            
    if extra_in_local:
        print("\nExtra in local dataset (possibly renamed/delisted):")
        for name in sorted(extra_in_local):
            print(f"- {name}")

    if not missing_in_local and not extra_in_local:
        print("\nBoth lists are identical!")

if __name__ == "__main__":
    main()
