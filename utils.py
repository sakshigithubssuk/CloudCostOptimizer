import json

def save_to_file(filename, data):
    try:
       
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(data, str):
                f.write(data)
            else:
                # here i used ensure_ascii=False to keeps symbols real
                json.dump(data, f, indent=2, ensure_ascii=False) 
        print(f"✅ Saved: {filename}")
    except Exception as e:
        print(f"❌ Error saving {filename}: {e}")

def load_json_file(filename):
    try:
        # I added encoding='utf-8' here too for the symbols like symbols for rupees
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return None
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
        return None