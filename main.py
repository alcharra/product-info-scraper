import json
from dotenv import load_dotenv
from utils.parser import determine_website_and_get_info
from utils.html_generator import generate_html
from utils.helpers import load_data, save_html, save_product_info, calculate_totals

load_dotenv()

def main():
    try:
        with open('config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            categories = config.get("categories", [])
            base_currency = config["convertOriginalCurrency"]["ExchangeFrom"]
            target_currencies = config["convertOriginalCurrency"]["ExchangeTo"]
            enable_conversion = config["convertOriginalCurrency"].get("enableConversion", True)
    except FileNotFoundError:
        print("config.json file not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding config.json: {e}")
        return

    actions = ["Add items", "Export items", "Exit"]
    
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
                    
                    product_info = determine_website_and_get_info(url, base_currency, target_currencies, enable_conversion)
                    
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
            html_content = generate_html(data, totals, base_currency, target_currencies)
            save_html(html_content, 'product_list.html')
            print("HTML report generated successfully.")
        elif action == 'exit':
            break
        else:
            print("Invalid action. Please choose 'export', 'add', or 'exit'.")

if __name__ == "__main__":
    main()
