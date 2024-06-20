import requests
import time
from utils.constants import HEADERS

def fetch_product_page(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Failed to retrieve the webpage (attempt {attempt + 1}): {e}")
            time.sleep(delay)
    print("Exceeded maximum retry attempts")
    return None
