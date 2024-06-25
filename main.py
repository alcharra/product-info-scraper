import json
from dotenv import load_dotenv
from utils.parser import determine_website_and_get_info
from utils.html_generator import generate_html
from utils.helpers import load_data, save_html, save_product_info, calculate_totals, rescan_prices

load_dotenv()

def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            categories = config.get("categories", [])
            base_currency = config["convertOriginalCurrency"]["ExchangeFrom"]
            target_currencies = config["convertOriginalCurrency"]["ExchangeTo"]
            enable_conversion = config["convertOriginalCurrency"].get("enableConversion", True)
            enable_auto_scan = config.get("enableAutoScan", False)
            return categories, base_currency, target_currencies, enable_conversion, enable_auto_scan
    except FileNotFoundError:
        print("config.json file not found.")
        return None, None, None, None, None
    except json.JSONDecodeError as e:
        print(f"Error decoding config.json: {e}")
        return None, None, None, None, None

def perform_rescan():
    data = load_data('./db/data.json')
    if not data:
        print("No data to rescan.")
        return
    print("Rescanning prices...")
    updated_data = rescan_prices(data, determine_website_and_get_info)
    if updated_data:
        with open('./db/data.json', 'w', encoding='utf-8') as file:
            json.dump(updated_data, file, ensure_ascii=False, indent=4)
        print("Prices rescanned and data.json updated successfully.")
    else:
        print("No price changes detected during rescan.")

def main():
    categories, base_currency, target_currencies, enable_conversion, enable_auto_scan = load_config()
    if categories is None:
        return

    if enable_auto_scan:
        perform_rescan()

    actions = ["Add items", "Export items", "Rescan Prices", "Exit"]

    while True:
        print("Please select an action:")
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")

        try:
            action_index = int(input("Enter the number corresponding to the action: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if action_index < 1 or action_index > len(actions):
            print("Invalid action number")
            continue

        action = actions[action_index - 1].lower().split()[0]

        if action == 'add':
            while True:
                print("Please select the category:")
                for i, category in enumerate(categories, 1):
                    print(f"{i}. {category}")
                print(f"{len(categories) + 1}. Go back to main menu")

                try:
                    category_index = int(input("Enter the number corresponding to the category: ").strip())
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if category_index == len(categories) + 1:
                    break

                if category_index < 1 or category_index > len(categories):
                    print("Invalid category number")
                    continue

                category = categories[category_index - 1]
                while True:
                    url = input("Please enter the product URL (or type 'back' to change category): ").strip()
                    if url.lower() == 'back':
                        break

                    product_info = determine_website_and_get_info(url)

                    if product_info:
                        save_product_info(product_info, category)
                    else:
                        print("Failed to retrieve product information. Please try again.")
        elif action == 'export':
            data = load_data('./db/data.json')
            if not data:
                print("No data to export.")
                continue
            totals = calculate_totals(data)
            html_content = generate_html(data, totals, base_currency, enable_conversion, target_currencies)
            save_html(html_content, 'product_list.html')
            print("HTML report generated successfully.")
        elif action == 'rescan':
            perform_rescan()
        elif action == 'exit':
            break
        else:
            print("Invalid action. Please choose 'export', 'add', 'rescan', or 'exit'.")

if __name__ == "__main__":
    main()
