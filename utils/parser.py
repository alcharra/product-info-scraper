from bs4 import BeautifulSoup
from utils.fetch import fetch_product_page
from utils.websites import get_ikea_product_info, get_elgiganten_product_info, get_trademax_product_info

def determine_website_and_get_info(url, base_currency, target_currency):
    content = fetch_product_page(url)
    if not content:
        return None
    
    soup = BeautifulSoup(content, 'html.parser')
    if 'ikea.com' in url:
        return get_ikea_product_info(url, soup, base_currency, target_currency)
    elif 'elgiganten.se' in url:
        return get_elgiganten_product_info(url, soup, base_currency, target_currency)
    elif 'trademax.se' in url:
        return get_trademax_product_info(url, soup, base_currency, target_currency)
    else:
        print("Unsupported website")
        return None
