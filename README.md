
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

```bash
pip install requests beautifulsoup4 lxml jinja2 python-dotenv
```

- An API key from ExchangeRate-API to fetch the exchange rates.

## Configuration

### `config.json`

Create a `config.json` file in the project directory with the following structure:

```json
{
  "categories": ["Kitchen", "Living Room", "Bedroom", "Bathroom"],
  "convertOriginalCurrency": {
    "ExchangeFrom": "SEK",
    "ExchangeTo": "GBP"
  }
}
```

- `categories`: List of product categories.
- `convertOriginalCurrency`: Configuration for currency conversion.
  - `ExchangeFrom`: The original currency code.
  - `ExchangeTo`: The target currency code.

## How to Use

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. Set Up the Environment

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Add Your API Key

Obtain your API key from ExchangeRate-API and create a `.env` file in the project directory with the following content:

```
EXCHANGE_RATE_API_KEY=your_api_key_here
```

### 4. Run the Script

You can either add product information or export the collected data into an HTML file.

#### Adding Product Information

1. Run the `main.py` script:

```bash
python main.py
```

2. When prompted, choose the action by entering the corresponding number:
   - 1. Add items
   - 2. Export items

3. If adding items, select the category by entering the corresponding number:
   - 1. Kitchen
   - 2. Living Room
   - 3. Bedroom
   - 4. Bathroom

4. Enter the product URLs one by one. Type `exit` to stop adding products.

#### Exporting Data

1. Run the `main.py` script:

```bash
python main.py
```

2. When prompted, choose the action by entering the corresponding number:
   - 1. Add items
   - 2. Export items

3. If exporting, the HTML report (`product_list.html`) will be generated in the current directory.

## Adding Support for a New Website

To add support for a new website, follow these steps:

1. Open `utils/websites.py`.
2. Define a new function to scrape product information from the new website. This function should accept `url`, `soup`, `base_currency`, and `target_currency` as parameters.
3. Parse the product information (name, price, image URL) within the new function.
4. Add the new function to the `determine_website_and_get_info` function in `utils/parser.py`.

### Example

```python
def get_newwebsite_product_info(url, soup, base_currency, target_currency):
    # Parse the product name, price, and image URL from the new website's page structure
    name_tag = soup.find('div', {'class': 'product-name'})
    price_tag = soup.find('span', {'class': 'price'})
    img_tag = soup.find('img', {'class': 'product-image'})
    
    if not name_tag or not price_tag or not img_tag:
        print("Failed to retrieve product information from NewWebsite.")
        return None
    
    name = name_tag.text.strip()
    original_price = parse_price(price_tag.text.strip())
    if original_price is None:
        print("Failed to parse the price for NewWebsite product.")
        return None

    exchange_rate = get_exchange_rate(base_currency, target_currency)
    if exchange_rate is None:
        print("Failed to retrieve exchange rate for NewWebsite product.")
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
```

## Warning

Please make sure to only scrape websites that allow it. Web scraping can be illegal and violate the terms of service of some websites.
