def calculate_totals(data):
    totals = {}
    overall_original_total = 0
    overall_exchange_total = 0
    for category, items in data.items():
        original_total = 0
        exchange_total = 0
        for item in items.values():
            original_price = float(item['original_price'].split()[0])
            exchange_price = float(item['exchange_price'].split()[0])
            original_total += original_price
            exchange_total += exchange_price
        totals[category] = {'original_total': original_total, 'exchange_total': exchange_total}
        overall_original_total += original_total
        overall_exchange_total += exchange_total
    totals['overall'] = {'original_total': overall_original_total, 'exchange_total': overall_exchange_total}
    return totals
