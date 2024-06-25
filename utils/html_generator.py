from jinja2 import Template
import datetime
from utils.helpers import get_exchange_prices

def generate_html(data, totals, base_currency, enable_conversion, target_currencies):
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    exchange_rate_cache = {}

    def get_cached_exchange_prices(price, base_currency, target_currencies, enable_conversion):
        if not enable_conversion:
            return {}
        cache_key = f"{price}_{base_currency}_{target_currencies}"
        if cache_key not in exchange_rate_cache:
            exchange_rate_cache[cache_key] = get_exchange_prices(price, base_currency, target_currencies, enable_conversion)
        return exchange_rate_cache[cache_key]

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
            .item-count { font-weight: bold; color: #333; }

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
                {% set overall_exchange_totals = get_cached_exchange_prices(totals['overall']['original_total'], base_currency, target_currencies, enable_conversion) %}
                {% for currency, total in overall_exchange_totals.items() %}
                    <div>Total {{ currency }}: {{ "%.2f" % total }}</div>
                {% endfor %}
            </div>
            {% for category, items in data.items() %}
            {% if items %}
            <div class="category">
                <h2>{{ category }}</h2>
                <div class="category-total">Total {{ base_currency }}: {{ "%.2f" % totals[category]['original_total'] }}
                {% set category_exchange_totals = get_cached_exchange_prices(totals[category]['original_total'], base_currency, target_currencies, enable_conversion) %}
                {% for currency, total in category_exchange_totals.items() %}
                    | Total {{ currency }}: {{ "%.2f" % total }}
                {% endfor %}
                </div>
                <div class="items">
                    {% set grouped_items = {} %}
                    {% for item in items.values() %}
                        {% if item.name in grouped_items %}
                            {% set grouped_items = grouped_items.update({item.name: grouped_items[item.name] + [item]}) %}
                        {% else %}
                            {% set grouped_items = grouped_items.update({item.name: [item]}) %}
                        {% endif %}
                    {% endfor %}
                    {% for item_name, item_list in grouped_items.items() %}
                    {% set item_count = item_list | count %}
                    {% set first_item = item_list[0] %}
                    <div class="item">
                        <img src="{{ first_item.picture_url }}" alt="{{ item_name }}" loading="lazy">
                        <div class="item-details">
                            <div><strong>{{ item_name }}</strong></div>
                            <div>{{ base_currency }} Price: {{ first_item.price }}</div>
                            <div class="item-count">Quantity: {{ item_count }}</div>
                            {% if item_count > 1 %}
                            <div class="item-total-price">{{ base_currency }} Total Price: {{ "%.2f" % (first_item.price.split()[0]|float * item_count) }}</div>
                            {% endif %}
                            {% set exchange_prices = get_cached_exchange_prices(first_item.price.split()[0]|float, base_currency, target_currencies, enable_conversion) %}
                            {% for currency, price in exchange_prices.items() %}
                                <div>{{ currency }} Price: {{ "%.2f" % price }}</div>
                                {% if item_count > 1 %}
                                <div class="item-total-price">{{ currency }} Total Price: {{ "%.2f" % (price * item_count) }}</div>
                                {% endif %}
                            {% endfor %}
                            <div><a href="{{ first_item.url }}" target="_blank">Product Link</a></div>
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
    return template.render(
        data=data, 
        totals=totals, 
        base_currency=base_currency, 
        target_currencies=target_currencies, 
        enable_conversion=enable_conversion,
        timestamp=timestamp, 
        get_cached_exchange_prices=get_cached_exchange_prices
    )
