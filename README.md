# Product Info Scraper and Exporter

## Overview

This project contains a script (`main.py`) that scrapes product information from specific e-commerce websites, saves the details in a JSON file, and exports the collected data into an HTML report. The supported websites are IKEA, Elgiganten, and Trademax.

### Features

- **Scrape Product Information**: Extracts product details such as name, price (in original and target currencies), and image URL.
- **Save Data**: Stores the scraped data in a structured JSON file categorised by product types.
- **Export Data**: Generates an HTML report summarising the collected product information.

## Supported Websites

- **IKEA** (https://www.ikea.com/)
- **Elgiganten** (https://www.elgiganten.se/)
- **Trademax** (https://www.trademax.se/)

## Prerequisites

- Python 3.x
- Required Python packages (can be installed using `pip`):

``` 
pip install requests beautifulsoup4 lxml jinja2 python-dotenv
``` 

- An API key from ExchangeRate-API to fetch the exchange rates.

## Configuration

### `config.json`

Create a `config.json` file in the project directory with the following structure:

``` json
{
  "categories": ["Kitchen", "Living Room", "Bedroom", "Bathroom"],
  "convertOriginalCurrency": {
    "enableConversion": true,
    "ExchangeFrom": "SEK",
    "ExchangeTo": ["GBP", "USD", "JPY"]
  }
}
```

- `categories`: List of product categories.
- `convertOriginalCurrency`: Configuration for currency conversion.
  - `enableConversion`: Boolean flag to enable or disable currency conversion.
  - `ExchangeFrom`: The original currency code.
  - `ExchangeTo`: List of target currency codes.

## How to Use

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

``` 
git clone <repository_url>
cd <repository_folder>
``` 

### 2. Set Up the Environment

Install the required Python packages:

``` 
pip install -r requirements.txt
``` 

### 3. Add Your API Key

Obtain your API key from ExchangeRate-API and create a `.env` file in the project directory with the following content:

``` 
EXCHANGE_RATE_API_KEY=your_api_key_here
``` 

### 4. Run the Script

You can either add product information, export the collected data into an HTML file, or rescan existing data.

#### Adding Product Information

1. Run the `main.py` script:

``` 
python main.py
``` 

2. When prompted, choose the action by entering the corresponding number:
   - 1. Add items
   - 2. Export items
   - 3. Rescan items
   - 4. Exit

3. If adding items, select the category by entering the corresponding number:
   - 1. Kitchen
   - 2. Living Room
   - 3. Bedroom
   - 4. Bathroom
   - 5. Go back to main menu

4. Enter the product URLs one by one. Type `back` to change category.

#### Exporting Data

1. Run the `main.py` script:

``` 
python main.py
``` 

2. When prompted, choose the action by entering the corresponding number:
   - 1. Add items
   - 2. Export items
   - 3. Rescan items
   - 4. Exit

3. If exporting, the HTML report (`product_list.html`) will be generated in the current directory.

#### Rescanning Data

1. Run the `main.py` script:

``` 
python main.py
``` 

2. When prompted, choose the action by entering the corresponding number:
   - 1. Add items
   - 2. Export items
   - 3. Rescan items
   - 4. Exit

3. If rescanning, the script will check for any price changes in the existing data and update the `data.json` file if there are any changes.

## Adding Support for a New Website

To add support for a new website, follow these steps:

1. Open `utils/websites.py`.
2. Define a new function to scrape product information from the new website. This function should accept `url`, `soup`, `base_currency`, `target_currencies`, and `enable_conversion` as parameters.
3. Parse the product information (name, price, image URL) within the new function.
4. Add the new function to the `determine_website_and_get_info` function in `utils/parser.py`.

### Example using CSS Selectors

``` 
def get_newwebsite_product_info(url, soup, base_currency, target_currencies, enable_conversion):
    name_selector = 'div.product-name'
    price_selector = 'span.price'
    img_selector = 'img.product-image'

    return get_product_info(
        url, 
        soup, 
        name_selector,
        price_selector,
        img_selector,
        base_currency, 
        target_currencies, 
        enable_conversion
    )
``` 

### Example using XPath

``` 
def get_newwebsite_product_info_xpath(url, soup, base_currency, target_currencies, enable_conversion):
    name_xpath = '//div[@class="product-name"]'
    price_xpath = '//span[@class="price"]'
    img_xpath = '//img[@class="product-image"]'

    return get_product_info_xpath(
        url,
        soup,
        name_xpath,
        price_xpath,
        img_xpath,
        base_currency,
        target_currencies,
        enable_conversion
    )
``` 

### Updating the Parser

In `utils/parser.py`, update the `determine_website_and_get_info` function to include the new website:

``` 
from utils.websites import get_ikea_product_info, get_elgiganten_product_info, get_trademax_product_info, get_newwebsite_product_info

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
    elif 'newwebsite.com' in url:
        return get_newwebsite_product_info(url, soup, base_currency, target_currencies, enable_conversion)
    else:
        print("Unsupported website")
        return None
``` 

## Warning

Please make sure to only scrape websites that allow it. Web scraping can be illegal and violate the terms of service of some websites.
