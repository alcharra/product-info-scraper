# Product Info Scraper and Exporter

## Overview

This project contains two scripts (`index.py` and `export.py`) that work together to scrape product information from specific e-commerce websites, save the details in a JSON file, and export the collected data into an HTML report. The supported websites are IKEA, Elgiganten, and Trademax.

### Features

- **Scrape Product Information**: Extracts product details such as name, price (in SEK and GBP), and image URL.
- **Save Data**: Stores the scraped data in a structured JSON file categorized by product types.
- **Export Data**: Generates an HTML report summarizing the collected product information.

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

1. Run the `index.py` script:

   ```bash
   python index.py
   ```

2. When prompted, choose the action `add` to add new products.
3. Enter the number corresponding to the category for the products:
   - 1. Kitchen
   - 2. Living Room
   - 3. Bedroom
   - 4. Bathroom
   - 5. Extra
4. Enter the product URLs one by one. Type `exit` to stop adding products.

#### Exporting Data

1. Run the `index.py` script:

   ```bash
   python index.py
   ```

2. When prompted, choose the action `export` to generate the HTML report.

The HTML report (`product_list.html`) will be generated in the current directory.

## Script Details

### `index.py`

This script handles the user interaction, fetching, and parsing of product information from the supported websites.

#### Functions

- `test_webpage_content(soup)`: Saves the webpage content to `test.html` for testing purposes.
- `get_exchange_rate(base_currency, target_currency)`: Fetches the exchange rate between two currencies.
- `fetch_product_page(url, retries=3, delay=5)`: Fetches the product page content with retry logic.
- `parse_price(price_str)`: Parses the price from a string to a float.
- `get_ikea_product_info(url, soup)`: Extracts product information from an IKEA product page.
- `get_elgiganten_product_info(url, soup)`: Extracts product information from an Elgiganten product page.
- `get_trademax_product_info(url, soup)`: Extracts product information from a Trademax product page.
- `save_product_info(product_info, category)`: Saves product information to the JSON file.
- `determine_website_and_get_info(url)`: Determines the website and fetches product information accordingly.
- `main()`: Main function to run the script.

### `export.py`

This script handles the loading of data from the JSON file, calculating totals, generating HTML, and saving the HTML report.

#### Functions

- `load_data(file_path)`: Loads data from a JSON file.
- `calculate_totals(data)`: Calculates the total prices in SEK and GBP for each category and overall.
- `generate_html(data, totals)`: Generates an HTML report from the data and totals.
- `save_html(html_content, file_path)`: Saves the generated HTML content to a file.
- `main()`: Main function to run the script independently if needed.

## Example Usage

### Adding Products

```bash
$ python index.py
Do you want to 'export' or 'add' items? add
Please select the category:
1. Kitchen
2. Living Room
3. Bedroom
4. Bathroom
5. Extra
Enter the number corresponding to the category: 1
Please enter the product URL (or type 'exit' to stop): https://www.ikea.com/se/sv/p/product1
Product information saved to Kitchen category in data.json
Please enter the product URL (or type 'exit' to stop): exit
```

### Exporting Data

```bash
$ python index.py
Do you want to 'export' or 'add' items? export
HTML report generated successfully.
```
