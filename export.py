import json
from jinja2 import Template

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def calculate_totals(data):
    totals = {}
    overall_sek_total = 0
    overall_gbp_total = 0
    for category, items in data.items():
        sek_total = 0
        gbp_total = 0
        for item in items.values():
            sek_price = float(item['sek_price'].split()[0])
            gbp_price = float(item['gbp_price'].split()[0])
            sek_total += sek_price
            gbp_total += gbp_price
        totals[category] = {'sek_total': sek_total, 'gbp_total': gbp_total}
        overall_sek_total += sek_total
        overall_gbp_total += gbp_total
    totals['overall'] = {'sek_total': overall_sek_total, 'gbp_total': overall_gbp_total}
    return totals

def generate_html(data, totals):
    html_template = """
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Product List</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; padding: 20px; background-color: #f5f5f5; }
            .container { max-width: 800px; width: 100%; background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            .overall-total { font-weight: bold; margin-bottom: 20px; color: #333; display: flex; justify-content: space-between; }
            .category { margin-top: 20px; }
            .category h2 { margin-bottom: 5px; color: #333; }
            .category-total { font-weight: bold; margin-bottom: 10px; color: #555; }
            .items { display: flex; flex-wrap: wrap; }
            .item { flex: 1 1 45%; margin: 10px; padding: 10px; border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.05); background: #f0f0f0; word-wrap: break-word; }
            .item:nth-of-type(odd) { background: #fafafa; }
            .item img { width: 100px; height: 100px; margin-right: 15px; border-radius: 5px; object-fit: cover; }
            .item-details { }
            .item-details div { margin-bottom: 5px; }

            @media (max-width: 600px) {
                .item { flex: 1 1 45%; }
                .item img { width: 100%; height: auto; margin-bottom: 10px; }
                .item-details { width: 100%; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="overall-total">
                <div>Total SEK: {{ "%.2f" % totals.overall.sek_total }}</div>
                <div>Total GBP: {{ "%.2f" % totals.overall.gbp_total }}</div>
            </div>
            {% for category, items in data.items() %}
            <div class="category">
                <h2>{{ category }}</h2>
                <div class="category-total">Total SEK: {{ "%.2f" % totals[category].sek_total }} | Total GBP: {{ "%.2f" % totals[category].gbp_total }}</div>
                <div class="items">
                    {% for item in items.values() %}
                    <div class="item">
                        <img src="{{ item.picture_url }}" alt="{{ item.name }}" loading="lazy">
                        <div class="item-details">
                            <div><strong>{{ item.name }}</strong></div>
                            <div>SEK Price: {{ item.sek_price }}</div>
                            <div>GBP Price: {{ item.gbp_price }}</div>
                            <div><a href="{{ item.url }}" target="_blank">Product Link</a></div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """

    template = Template(html_template)
    return template.render(data=data, totals=totals)

def save_html(html_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

def main():
    data_file = 'data.json'
    output_file = 'product_list.html'
    
    data = load_data(data_file)
    totals = calculate_totals(data)
    html_content = generate_html(data, totals)
    save_html(html_content, output_file)
    
    print(f"HTML file saved to {output_file}")

if __name__ == "__main__":
    main()
