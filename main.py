import json
from dotenv import load_dotenv
from utils.parser import determine_website_and_get_info
from utils.data_loader import load_data
from utils.totals_calculator import calculate_totals
from utils.html_generator import generate_html
from utils.save import save_html, save_product_info

load_dotenv()

def main():
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
        categories = config.get("categories", [])
        base_currency = config["convertOriginalCurrency"]["ExchangeFrom"]
        target_currency = config["convertOriginalCurrency"]["ExchangeTo"]

    actions = ["Add items", "Export items"]
    
    print("Please select an action:")
    for i, action in enumerate(actions, 1):
        print(f"{i}. {action}")
    
    action_index = int(input("Enter the number corresponding to the action: ").strip())
    
    if action_index < 1 or action_index > len(actions):
        print("Invalid action number")
        return
    
    action = actions[action_index - 1].lower().split()[0]
    
    if action == 'add':
        print("Please select the category:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        
        category_index = int(input("Enter the number corresponding to the category: ").strip())
        
        if category_index < 1 or category_index > len(categories):
            print("Invalid category number")
        else:
            category = categories[category_index - 1]
            while True:
                url = input("Please enter the product URL (or type 'exit' to stop): ").strip()
                if url.lower() == 'exit':
                    break
                
                product_info = determine_website_and_get_info(url, base_currency, target_currency)
                
                if product_info:
                    save_product_info(product_info, category)
                else:
                    print("Failed to retrieve product information. Please try again.")
    elif action == 'export':
        data = load_data('./db/data.json')
        totals = calculate_totals(data)
        html_content = generate_html(data, totals, base_currency, target_currency)
        save_html(html_content, 'product_list.html')
        print("HTML report generated successfully.")
    else:
        print("Invalid action. Please choose 'export' or 'add'.")

if __name__ == "__main__":
    main()
