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