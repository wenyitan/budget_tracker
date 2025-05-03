def format_breakdown_message(breakdown):
    text = ""
    total = 0
    for cat in breakdown:
        category = cat['category']
        amount = cat['amount']
        text += f"*{category}*: ${amount}\n"
        total += amount
    text += f"*Total*: ${total:.2f}"
    return text
