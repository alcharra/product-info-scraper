from bs4 import BeautifulSoup
from utils.exchange_rate import get_exchange_rate
from lxml import html

def parse_price(price_str):
    try:
        price = price_str.replace(' ', '').replace(':-', '').replace('kr', '').replace(',', '.').replace('.', '')
        price = price.replace('-', '')
        price = price.replace(' ', '')
        return float(price)
    except ValueError:
        print("Failed to parse the price")
        return None

def get_ikea_product_info(url, soup, base_currency, target_currency):
    name_tag = soup.find('span', {'class': 'pip-header-section__description-text'})
    if not name_tag:
        print("Failed to retrieve product name from IKEA.")
        return None

    price_tag = soup.find('span', {'class': 'pip-temp-price__integer'})
    if not price_tag:
        print("Failed to retrieve product price from IKEA.")
        return None

    img_tag = soup.find('img', {'class': 'pip-image'})
    if not img_tag or not img_tag.has_attr('src'):
        print("Failed to retrieve product picture from IKEA.")
        return None

    name = name_tag.text.strip()
    original_price = parse_price(price_tag.text.strip())
    if original_price is None:
        print("Failed to parse the price for IKEA product.")
        return None

    exchange_rate = get_exchange_rate(base_currency, target_currency)
    if exchange_rate is None:
        print("Failed to retrieve exchange rate for IKEA product.")
        return None

    exchange_price = original_price * exchange_rate
    picture_url = img_tag['src']

    return {
        'url': url,
        'name': name,
        'original_price': f"{original_price:.2f} {base_currency}",
        'exchange_price': f"{exchange_price:.2f} {target_currency}",
        'picture_url': picture_url
    }

def get_elgiganten_product_info(url, soup, base_currency, target_currency):
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
    original_price = parse_price(price_tag.text.strip())
    if original_price is None:
        print("Failed to parse the price for Elgiganten product.")
        return None

    exchange_rate = get_exchange_rate(base_currency, target_currency)
    if exchange_rate is None:
        print("Failed to retrieve exchange rate for Elgiganten product.")
        return None

    exchange_price = original_price * exchange_rate
    picture_url = img_tag['src']

    return {
        'url': url,
        'name': name,
        'original_price': f"{original_price:.2f} {base_currency}",
        'exchange_price': f"{exchange_price:.2f} {target_currency}",
        'picture_url': picture_url
    }

def get_trademax_product_info(url, soup, base_currency, target_currency):
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
    original_price = parse_price(price_tag[0].text.strip())
    if original_price is None:
        print("Failed to parse the price for Trademax product.")
        return None

    exchange_rate = get_exchange_rate(base_currency, target_currency)
    if exchange_rate is None:
        print("Failed to retrieve exchange rate for Trademax product.")
        return None

    exchange_price = original_price * exchange_rate
    picture_url = picture_tag[0].get('src')

    return {
        'url': url,
        'name': name,
        'original_price': f"{original_price:.2f} {base_currency}",
        'exchange_price': f"{exchange_price:.2f} {target_currency}",
        'picture_url': f"https://www.trademax.se{picture_url}"
    }
