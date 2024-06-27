import json
from dotenv import load_dotenv
from utils.parser import determine_website_and_get_info
from utils.generator.html import generate_html
from utils.helpers import load_data, load_config, perform_rescan
from utils.product.helpers import save_product_info
from utils.generator.helpers import save_html, calculate_totals

load_dotenv()

def main():
    categories, base_currency, target_currencies, enable_conversion, enable_auto_scan = load_config()
    if categories is None:
        return

    if enable_auto_scan:
        perform_rescan(determine_website_and_get_info)

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
            perform_rescan(determine_website_and_get_info)
        elif action == 'exit':
            break
        else:
            print("Invalid action. Please choose 'export', 'add', 'rescan', or 'exit'.")

if __name__ == "__main__":
    main()
