from lxml import html
from utils.product.helpers import parse_price, get_full_image_url

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