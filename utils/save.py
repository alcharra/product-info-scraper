import json
import os

def save_html(html_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

def save_product_info(product_info, category):
    data_file = './db/data.json'
    
    if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
        with open(data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {}

    if category not in data:
        data[category] = {}

    product_id = len(data[category]) + 1
    data[category][product_id] = product_info
    
    with open(data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    print(f"Product information saved to {category} category in data.json")
