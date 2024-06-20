from jinja2 import Template
import datetime

def generate_html(data, totals, base_currency, target_currencies):
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Product List</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; padding: 20px; background-color: #f5f5f5; }
            .container { max-width: 800px; width: 100%; background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            .timestamp { text-align: center; margin-bottom: 20px; color: #777; }
            .overall-total { font-weight: bold; margin-bottom: 20px; color: #333; display: flex; justify-content: space-between; }
            .category { margin-top: 20px; }
            .category h2 { margin-bottom: 5px; color: #333; }
            .category-total { font-weight: bold; margin-bottom: 10px; color: #555; }
            .items { display: flex; flex-wrap: wrap; }
            .item { flex: 1 1 45%; margin: 10px; padding: 10px; border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.05); background: #f0f0f0; word-wrap: break-word; }
            .item:nth-of-type(odd) { background: #fafafa; }
            .item img { width: 100px; height: 100px; margin-right: 15px; border-radius: 5px; object-fit: cover; }
            .item-details div { margin-bottom: 5px; }

            @media (max-width: 600px) {
                .item { flex: 1 1 100%; }
                .item img { width: 100%; height: auto; margin-bottom: 10px; }
                .item-details { width: 100%; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="timestamp">
                Report generated on: {{ timestamp }}
            </div>
            <div class="overall-total">
                <div>Total {{ base_currency }}: {{ "%.2f" % totals['overall']['original_total'] }}</div>
                {% for currency, total in totals['overall']['exchange_totals'].items() %}
                    <div>Total {{ currency }}: {{ "%.2f" % total }}</div>
                {% endfor %}
            </div>
            {% for category, items in data.items() %}
            {% if items %}
            <div class="category">
                <h2>{{ category }}</h2>
                <div class="category-total">Total {{ base_currency }}: {{ "%.2f" % totals[category]['original_total'] }}
                {% for currency, total in totals[category]['exchange_totals'].items() %}
                    | Total {{ currency }}: {{ "%.2f" % total }}
                {% endfor %}
                </div>
                <div class="items">
                    {% for item in items.values() %}
                    <div class="item">
                        <img src="{{ item.picture_url }}" alt="{{ item.name }}" loading="lazy">
                        <div class="item-details">
                            <div><strong>{{ item.name }}</strong></div>
                            <div>{{ base_currency }} Price: {{ item.original_price }}</div>
                            {% for currency in target_currencies %}
                                {% if item.get('exchange_price_' ~ currency) %}
                                    <div>{{ currency }} Price: {{ item['exchange_price_' ~ currency] }}</div>
                                {% endif %}
                            {% endfor %}
                            <div><a href="{{ item.url }}" target="_blank">Product Link</a></div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            {% endfor %}
        </div>
    </body>
    </html>
    """

    template = Template(html_template)
    return template.render(data=data, totals=totals, base_currency=base_currency, target_currencies=target_currencies, timestamp=timestamp)
