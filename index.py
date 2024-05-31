import requests
from bs4 import BeautifulSoup
import json
import os
import time
from lxml import html
from export import load_data, calculate_totals, generate_html, save_html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def test_webpage_content(soup):
    output_file = 'test.html'
    pretty_html = soup.prettify()
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(pretty_html)

def get_exchange_rate(api_key, base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve exchange rate: {e}")
        return None
    
    data = response.json()
    if 'conversion_rates' not in data or target_currency not in data['conversion_rates']:
        print("Invalid exchange rate data")
        return None
    
    return data['conversion_rates'][target_currency]

def fetch_product_page(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Failed to retrieve the webpage (attempt {attempt + 1}): {e}")
            time.sleep(delay)
    print("Exceeded maximum retry attempts")
    return None

def parse_price(price_str):
    try:
        price = price_str.replace(' ', '').replace(':-', '').replace('kr', '').replace(',', '.').replace('.', '')
        price = price.replace('-', '')
        price = price.replace(' ', '')
        return float(price)
    except ValueError:
        print("Failed to parse the SEK price")
        return None

def get_ikea_product_info(url, soup, api_key):
    name_tag = soup.find('span', class_='pip-header-section__description-text')
    if not name_tag:
        print("Failed to retrieve product name from IKEA.")
        return None

    price_tag = soup.find('span', class_='pip-temp-price__integer')
    if not price_tag:
        print("Failed to retrieve product price from IKEA.")
        return None

    picture_tag = soup.find('img', class_='pip-image')
    if not picture_tag:
        print("Failed to retrieve product picture tag from IKEA.")
        return None

    if not picture_tag.has_attr('src'):
        print("Product picture from IKEA does not have 'src' attribute.")
        return None

    name = name_tag.text.strip()
    sek_price = parse_price(price_tag.text.strip())
    if sek_price is None:
        print("Failed to parse the SEK price for IKEA product.")
        return None

    exchange_rate = get_exchange_rate(api_key, 'SEK', 'GBP')
    if exchange_rate is None:
        print("Failed to retrieve exchange rate for IKEA product.")
        return None

    gbp_price = sek_price * exchange_rate
    picture_url = picture_tag['src']

    return {
        'url': url,
        'name': name,
        'sek_price': f"{sek_price} SEK",
        'gbp_price': f"{gbp_price:.2f} GBP",
        'picture_url': picture_url
    }

def get_elgiganten_product_info(url, soup, api_key):
    name_tag = soup.find('span', class_='font-regular font-bold xl:text-4xl text-xl')
    if not name_tag:
        print("Failed to retrieve product name from Elgiganten.")
        return None

    price_tag = soup.find('span', class_='font-headline text-[3.5rem] leading-[3.5rem] inc-vat')
    if not price_tag:
        print("Failed to retrieve product price from Elgiganten.")
        return None

    li_tag = soup.find('li', class_='items-center flex snap-start pb-10')
    if not li_tag:
        print("Failed to retrieve product list item from Elgiganten.")
        return None

    img_tag = li_tag.find('img')
    if not img_tag:
        print("Failed to retrieve product picture tag from Elgiganten.")
        return None

    if not img_tag.has_attr('src'):
        print("Product picture from Elgiganten does not have 'src' attribute.")
        return None

    name = name_tag.text.strip()
    sek_price = parse_price(price_tag.text.strip())
    if sek_price is None:
        print("Failed to parse the SEK price for Elgiganten product.")
        return None

    exchange_rate = get_exchange_rate(api_key, 'SEK', 'GBP')
    if exchange_rate is None:
        print("Failed to retrieve exchange rate for Elgiganten product.")
        return None

    gbp_price = sek_price * exchange_rate
    picture_url = img_tag['src']

    return {
        'url': url,
        'name': name,
        'sek_price': f"{sek_price} SEK",
        'gbp_price': f"{gbp_price:.2f} GBP",
        'picture_url': picture_url
    }

def get_trademax_product_info(url, soup, api_key):
    tree = html.fromstring(str(soup))

    name_xpath = '/html/body/div[1]/div/main/div[2]/div[2]/div[1]/h1'
    price_xpath = '/html/body/div[1]/div/main/div[2]/div[2]/div[1]/div[2]/div[2]/div/div'
    picture_xpath = '/html/body/div[1]/div/main/div[2]/div[1]/div/div[2]/div[1]/div/div/div[1]/img'

    name_tag = tree.xpath(name_xpath)
    price_tag = tree.xpath(price_xpath)
    picture_tag = tree.xpath(picture_xpath)

    if not name_tag:
        print("Failed to retrieve product name from Trademax.")
        return None
    
    if not price_tag:
        print("Failed to retrieve product price from Trademax.")
        return None
    
    if not picture_tag:
        print("Failed to retrieve product picture tag from Trademax.")
        return None

    name = name_tag[0].text.strip()
    sek_price = parse_price(price_tag[0].text.strip())
    if sek_price is None:
        print("Failed to parse the SEK price for Trademax product.")
        return None

    exchange_rate = get_exchange_rate(api_key, 'SEK', 'GBP')
    if exchange_rate is None:
        print("Failed to retrieve exchange rate for Trademax product.")
        return None

    gbp_price = sek_price * exchange_rate
    picture_url = picture_tag[0].get('src')

    return {
        'url': url,
        'name': name,
        'sek_price': f"{sek_price} SEK",
        'gbp_price': f"{gbp_price:.2f} GBP",
        'picture_url': f"https://www.trademax.se{picture_url}"
    }

def save_product_info(product_info, category):
    data_file = 'data.json'
    
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {
            "Kitchen": {},
            "Living Room": {},
            "Bedroom": {},
            "Extra": {}
        }
    
    if category not in data:
        print("Invalid category")
        return
    
    product_id = len(data[category]) + 1
    data[category][product_id] = product_info
    
    with open(data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    print(f"Product information saved to {category} category in data.json")

def determine_website_and_get_info(url, api_key):
    content = fetch_product_page(url)
    if not content:
        return None
    
    soup = BeautifulSoup(content, 'html.parser')
    if 'ikea.com' in url:
        return get_ikea_product_info(url, soup, api_key)
    elif 'elgiganten.se' in url:
        return get_elgiganten_product_info(url, soup, api_key)
    elif 'trademax.se' in url:
        return get_trademax_product_info(url, soup, api_key)
    else:
        print("Unsupported website")
        return None

def main():
    api_key = "(ADD API KEY HERE)"
    action = input("Do you want to 'export' or 'add' items? ").strip().lower()
    
    if action == 'add':
        category = input("Please enter the category (Kitchen, Living Room, Bedroom, Bathroom, Extra): ").strip()
        
        if category not in ["Kitchen", "Living Room", "Bedroom", "Bathroom", "Extra"]:
            print("Invalid category")
        else:
            while True:
                url = input("Please enter the product URL (or type 'exit' to stop): ").strip()
                if url.lower() == 'exit':
                    break
                
                product_info = determine_website_and_get_info(url, api_key)
                
                if product_info:
                    save_product_info(product_info, category)
                else:
                    print("Failed to retrieve product information. Please try again.")
    elif action == 'export':
        data = load_data('data.json')
        totals = calculate_totals(data)
        html_content = generate_html(data, totals)
        save_html(html_content, 'product_list.html')
        print("HTML report generated successfully.")
    else:
        print("Invalid action. Please choose 'export' or 'add'.")

if __name__ == "__main__":
    main()
