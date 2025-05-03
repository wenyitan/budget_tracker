def format_breakdown_message(breakdown):
    text = ""
    for category, amount in breakdown.items():
        text += f"*{category}*: ${amount:.2f}\n" if category != "Shared" else f"(*{category}*: ${amount:.2f})\n"
    return text
