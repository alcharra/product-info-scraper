import re
import json
import os
import requests
import time
from tqdm import tqdm
from lxml import html
from urllib.parse import urljoin
from utils.constants import HEADERS
from utils.exchange_rate import get_exchange_rate

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return {}

def save_html(html_content, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
    except IOError as e:
        print(f"Error saving HTML to file: {file_path}. {e}")

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

def fetch_product_page(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Failed to retrieve the webpage (attempt {attempt + 1}): {e}")
            time.sleep(delay)
    print("Exceeded maximum retry attempts")
    return None

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

def get_exchange_prices(price, base_currency, target_currencies, enable_conversion):
    exchange_prices = {}
    if enable_conversion:
        for target_currency in target_currencies:
            exchange_rate = get_exchange_rate(base_currency, target_currency)
            if exchange_rate is None:
                print(f"Failed to retrieve exchange rate for {target_currency}.")
                continue
            exchange_prices[target_currency] = price * exchange_rate
    return exchange_prices

def get_full_image_url(base_url, img_src):
    if not img_src.startswith('http'):
        return urljoin(base_url, img_src)
    return img_src

def get_product_info(url, soup, name_selector, price_selector, img_selector):
    name_tag = soup.select_one(name_selector)
    price_tag = soup.select_one(price_selector)
    img_tag = soup.select_one(img_selector)

    if not name_tag:
        print(f"Failed to retrieve product name from {url}.")
        return None

    if not price_tag:
        print(f"Failed to retrieve product price from {url}.")
        return None

    if not img_tag or not img_tag.has_attr('src'):
        print(f"Failed to retrieve product picture from {url}.")
        return None

    name = name_tag.text.strip()
    price = parse_price(price_tag.text.strip())
    if price is None:
        print(f"Failed to parse the price for product from {url}.")
        return None

    product_info = {
        'url': url,
        'name': name,
        'price': f"{price:.2f}",
        'picture_url': img_tag['src']
    }

    return product_info

def get_product_info_xpath(url, soup, name_xpath, price_xpath, img_xpath):
    tree = html.fromstring(str(soup))
    name_tag = tree.xpath(name_xpath)
    price_tag = tree.xpath(price_xpath)
    img_tag = tree.xpath(img_xpath)

    if not name_tag:
        print(f"Failed to retrieve product name from {url}.")
        return None

    if not price_tag:
        print(f"Failed to retrieve product price from {url}.")
        return None

    if not img_tag:
        print(f"Failed to retrieve product picture from {url}.")
        return None

    name = name_tag[0].text.strip()
    price = parse_price(price_tag[0].text.strip())
    if price is None:
        print(f"Failed to parse the price for product from {url}.")
        return None

    picture_url = get_full_image_url(url, img_tag[0].get('src'))

    product_info = {
        'url': url,
        'name': name,
        'price': f"{price:.2f}",
        'picture_url': picture_url
    }

    return product_info

def calculate_totals(data):
    totals = {}
    overall_original_total = 0

    for category, items in data.items():
        original_total = 0

        for item in items.values():
            price = float(item['price'].split()[0])
            original_total += price

        totals[category] = {'original_total': original_total}
        overall_original_total += original_total

    totals['overall'] = {'original_total': overall_original_total}
    return totals

def rescan_prices(data, determine_website_and_get_info):
    updated_data = data.copy()
    changes = False
    for category, items in tqdm(data.items(), desc="Rescanning categories", unit="category"):
        print(f"\nRescanning items in {category}...")
        for item_id, item in tqdm(items.items(), desc="Rescanning items", unit="item", leave=False):
            url = item['url']
            try:
                new_product_info = determine_website_and_get_info(url)
                if new_product_info and new_product_info['price'] != item['price']:
                    updated_data[category][item_id] = new_product_info
                    changes = True
                    print(f"\nUpdated price for {item['name']} from {item['price']} to {new_product_info['price']}")
            except Exception as e:
                print(f"\nFailed to rescan product {item['name']} from {url}. Error: {e}")
    return updated_data if changes else None