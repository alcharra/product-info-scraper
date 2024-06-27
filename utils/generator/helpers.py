from utils.exchange_rate import get_exchange_rate

def calculate_totals(data):
    totals = {}
    overall_original_total = 0

    for category, items in data.items():
        original_total = 0

        for item in items.values():
            price = float(item['price'].split()[0])
            original_total += price

        totals[category] = {'original_total': original_total}
        overall_original_total += original_total

    totals['overall'] = {'original_total': overall_original_total}
    return totals

def get_exchange_prices(price, base_currency, target_currencies, enable_conversion):
    exchange_prices = {}
    if enable_conversion:
        for target_currency in target_currencies:
            exchange_rate = get_exchange_rate(base_currency, target_currency)
            if exchange_rate is None:
                print(f"Failed to retrieve exchange rate for {target_currency}.")
                continue
            exchange_prices[target_currency] = price * exchange_rate
    return exchange_prices
    
def save_html(html_content, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
    except IOError as e:
        print(f"Error saving HTML to file: {file_path}. {e}")