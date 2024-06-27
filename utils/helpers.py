import json
import requests
import time
from tqdm import tqdm
from utils.constants import HEADERS

def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            categories = config.get("categories", [])
            base_currency = config["convertOriginalCurrency"]["ExchangeFrom"]
            target_currencies = config["convertOriginalCurrency"]["ExchangeTo"]
            enable_conversion = config["convertOriginalCurrency"].get("enableConversion", True)
            enable_auto_scan = config.get("enableAutoScan", False)
            return categories, base_currency, target_currencies, enable_conversion, enable_auto_scan
    except FileNotFoundError:
        print("config.json file not found.")
        return None, None, None, None, None
    except json.JSONDecodeError as e:
        print(f"Error decoding config.json: {e}")
        return None, None, None, None, None
    
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

def perform_rescan(determine_website_and_get_info):
    data = load_data('./db/data.json')
    if not data:
        print("No data to rescan.")
        return
    print("Rescanning prices...")
    updated_data = rescan_prices(data, determine_website_and_get_info)
    if updated_data:
        with open('./db/data.json', 'w', encoding='utf-8') as file:
            json.dump(updated_data, file, ensure_ascii=False, indent=4)
        print("Prices rescanned and data.json updated successfully.")
    else:
        print("No price changes detected during rescan.")
