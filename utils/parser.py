from bs4 import BeautifulSoup
from utils.helpers import fetch_product_page
from utils.websites import get_ikea_product_info, get_elgiganten_product_info, get_trademax_product_info

def determine_website_and_get_info(url, base_currency, target_currencies, enable_conversion):
    content = fetch_product_page(url)
    if not content:
        return None
    
    soup = BeautifulSoup(content, 'html.parser')
    if 'ikea.com' in url:
        return get_ikea_product_info(url, soup, base_currency, target_currencies, enable_conversion)
    elif 'elgiganten.se' in url:
        return get_elgiganten_product_info(url, soup, base_currency, target_currencies, enable_conversion)
    elif 'trademax.se' in url:
        return get_trademax_product_info(url, soup, base_currency, target_currencies, enable_conversion)
    else:
        print("Unsupported website")
        return None
