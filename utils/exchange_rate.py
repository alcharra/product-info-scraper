import os
import requests
from utils.constants import HEADERS

def get_exchange_rate(base_currency, target_currency):
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve exchange rate: {e}")
        return None
    
    data = response.json()
    if 'conversion_rates' not in data or target_currency not in data['conversion_rates']:
        print("Invalid exchange rate data")
        return None
    
    return data['conversion_rates'][target_currency]
