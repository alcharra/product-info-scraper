from urllib.parse import urljoin
import re
import json
import os
def parse_price(price_str):
    try:
        price_str = re.sub(r'[^\d.,]', '', price_str)
        
        if re.search(r'\.\D|,\D', price_str):
            price_str = re.sub(r'\.\D|,\D', '', price_str)
        
        if ',' in price_str and '.' in price_str:
            if price_str.find(',') > price_str.find('.'):
                price_str = price_str.replace('.', '').replace(',', '.')
            else:
                price_str = price_str.replace(',', '')
        elif ',' in price_str:
            price_str = price_str.replace(',', '.')
        
        return float(price_str)
    except ValueError:
        print("Failed to parse the price")
        return None

def get_full_image_url(base_url, img_src):
    if not img_src.startswith('http'):
        return urljoin(base_url, img_src)
    return img_src

def save_product_info(product_info, category):
    data_file = './db/data.json'
    
    try:
        if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
            with open(data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {}
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading data file: {e}")
        data = {}

    if category not in data:
        data[category] = {}

    product_id = len(data[category]) + 1
    data[category][product_id] = product_info
    
    try:
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Product information saved to {category} category in data.json")
    except IOError as e:
        print(f"Error saving product information to file: {e}")