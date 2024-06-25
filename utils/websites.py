from utils.helpers import get_product_info, get_product_info_xpath

def get_ikea_product_info(url, soup):
    name_selector = 'span.pip-header-section__description-text'
    price_selector = 'span.pip-temp-price__integer'
    img_selector = 'img.pip-image'

    return get_product_info(
        url, 
        soup, 
        name_selector,
        price_selector,
        img_selector
    )

def get_elgiganten_product_info(url, soup):
    name_selector = 'span.font-regular.font-bold.xl\\:text-4xl.text-xl'
    price_selector = 'span.font-headline.text-\\[3\\.5rem\\].leading-\\[3\\.5rem\\].inc-vat'
    img_selector = 'li.items-center.flex.snap-start.pb-10 img'

    return get_product_info(
        url, 
        soup, 
        name_selector,
        price_selector,
        img_selector
    )

def get_trademax_product_info(url, soup):
    name_xpath = '/html/body/div[1]/div/main/div[2]/div[2]/div[1]/h1'
    price_xpath = '/html/body/div[1]/div/main/div[2]/div[2]/div[1]/div[2]/div/div/div'
    img_xpath = '/html/body/div[1]/div/main/div[2]/div[1]/div/div[2]/div[1]/div/div/div[1]/img'

    return get_product_info_xpath(
        url,
        soup,
        name_xpath,
        price_xpath,
        img_xpath
    )

def get_chilli_product_info(url, soup):
    name_xpath = '/html/body/div[1]/div/main/div[2]/div[2]/div[1]/h1'
    price_xpath = '/html/body/div[1]/div/main/div[2]/div[2]/div[1]/div[2]/div[2]/span[2]'
    img_xpath = '/html/body/div[1]/div/main/div[2]/div[1]/div/div[2]/div[1]/div/div/div[1]/img'

    return get_product_info_xpath(
        url,
        soup,
        name_xpath,
        price_xpath,
        img_xpath
    )
