import datetime

now = datetime.datetime.now().year

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

months_day_map = {
    "Jan": 31,
    "Feb": 29 if is_leap_year(now) else 28,
    "Mar": 31,
    "Apr": 30,
    "May": 31,
    "Jun": 31,
    "Jul": 30,
    "Aug": 31,
    "Sep": 30,
    "Oct": 31,
    "Nov": 30,
    "Dec": 31,
}

# def generate_message_table(transactions):
#     table = ""
#     headers = transactions[0].keys()

#     dimensions = {key:0 for key in headers}
#     for key in dimensions.keys():
#         strings = list(map(lambda x: str(x[key]) if key != "shared" else "yes" if x[key] == 1 else "false", transactions))
#         strings.append(key)
#         max_length = max(map(lambda x: len(x), strings))
#         # max_length = max_length if max_length % 2 == 0 else max_length + 1
#         dimensions[key] = max_length 

#     header = "| "
#     for heading in headers:
#         header += heading.center(dimensions[heading]) + " | "
#     table += header + "\n"

#     for transaction in transactions:
#         line = "| "
#         for key in transaction.keys():
#             text = str(transaction[key]) if key != "shared" else "yes" if transaction[key] == 1 else "no"
#             line += text.center(dimensions[key]) + " | "
#         table += line + "\n"
#     return table