import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, WMonthTelegramCalendar, LSTEP
from telebot.util import quick_markup
import datetime
from config import BOT_TOKEN, ALLOWED_USERS, DATE_FORMAT
from utils import months_day_map
from transaction import Transaction

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    from_user = message.from_user
    chat = message.chat
    if from_user.id in ALLOWED_USERS:
        bot.send_message(chat.id, text=f"Hello {from_user.first_name}. Please use /log to log an expense. Other commands you can use are:")
    else:
        print("NOT AUTHORISED")

@bot.message_handler(commands=['log'])
def log(message):
    from_user = message.from_user
    chat = message.chat
    text = "How much was spent?"
    if from_user.id in ALLOWED_USERS:
        sent_message = bot.send_message(chat.id, text=text)
        bot.register_next_step_handler(sent_message, register_amount_prompt_person)
    else:
        print("NOT AUTHORISED")

def register_amount_prompt_person(message):
    chat = message.chat
    try:
        amount = float(message.text)
        transaction = Transaction(amount=amount)
        text = f"Ok, ${amount} was spent. Who spent it? Wens or Tians?"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Wens")
        markup.add("Tians")
        sent_message = bot.send_message(chat.id, text=text, reply_markup=markup)
        bot.register_next_step_handler(message=sent_message, callback=register_person_prompt_date, transaction=transaction)
    except ValueError:
        pass

def register_person_prompt_date(message, **kwargs):
    chat = message.chat
    person = message.text
    if person not in ["Wens", "Tians"]:
        markup = types.ReplyKeyboardRemove()
        text = "If you are Wens or Tians, please use the options given. If you are not then you shouldn't be here!!"
        bot.send_message(chat.id, text=text, reply_markup=markup)
    else:
        transaction = kwargs['transaction']
        transaction.person = person
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Yes")
        markup.add("No")
        text = f"OK. Is it a shared transaction"
        sent_message = bot.send_message(chat.id, text=text, reply_markup=markup)
        bot.register_next_step_handler(message=sent_message, callback=handle_shared_yes_no, transaction=transaction)

def handle_today_yes_no(message, **kwargs):
    chat = message.chat
    answer = message.text
    transaction = kwargs['transaction']
    date = datetime.datetime.now().strftime(DATE_FORMAT)
    if answer == "Yes":
        transaction.date = date
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Yes")
        markup.add("No")
        text = "OK. Do you have any comments?"
        sent_message = bot.send_message(chat.id, text=text, reply_markup=markup)
        bot.register_next_step_handler(message=sent_message, callback=handle_shared_yes_no, transaction=transaction)
    elif answer == "No":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        month = date.split("-")[1]
        days = list(map(lambda i : str(i) if i > 9 else "0"+ str(i), range(1, months_day_map[month] + 1))) 
        markup.add(*days, row_width=6)
        sent_message = bot.send_message(message.chat.id,
                     f"Ok which day?",
                     reply_markup=markup)
        bot.register_next_step_handler(message=sent_message, callback=handle_day_prompt_month, transaction=transaction)
    else:
        pass

def handle_day_prompt_month(message, **kwargs):
    chat = message.chat
    day = message.text
    transaction = kwargs['transaction']
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(*months_day_map.keys(), row_width=3)
    # for month in months_day_map.keys():
    #     markup.add(month)
    text = "Which month was it?"
    sent_message = bot.send_message(chat.id, text=text, reply_markup=markup)
    bot.register_next_step_handler(message=sent_message, callback=handle_month_prompt_year, transaction=transaction, day=day)

def handle_month_prompt_year(message, **kwargs):
    chat = message.chat
    month = message.text
    day = kwargs['day']
    transaction = kwargs['transaction']
    text = "Which year was it? (Please type and provide a 4-digit year)"
    sent_message = bot.send_message(chat.id, text=text)
    bot.register_next_step_handler(message=sent_message, callback=handle_year_prompt_shared, transaction=transaction, day=day, month=month)

def handle_year_prompt_shared(message, **kwargs):
    chat = message.chat
    year = message.text
    month = kwargs['month']
    day = kwargs['day']
    transaction = kwargs['transaction']
    transaction.date = f"{day}-{month}-{year}"
    print(transaction.date)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Yes")
    markup.add("No")
    text = "OK. Do you have any comments?"
    sent_message = bot.send_message(chat.id, text=text, reply_markup=markup)
    bot.register_next_step_handler(message=sent_message, callback=handle_shared_yes_no, transaction=transaction)


def handle_shared_yes_no(message, **kwargs):
    print(kwargs['transaction'].__dict__)
    answer = message.text.lower()
    transaction = kwargs['transaction']
    transaction.shared = answer == "yes"


if __name__ == "__main__":
    print("starting bot")
    bot.infinity_polling()