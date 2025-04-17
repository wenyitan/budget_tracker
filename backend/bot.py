from config import BOT_TOKEN, expense_categories, allowed_users
import asyncio
import telebot
from telebot.util import quick_markup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import utils
from models import Transaction

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    userId = str(message.from_user.id)
    if userId not in allowed_users:
        text = "Sorry, you are not authorised for this command!!"
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(chat_id=utils.get_chat_id(message), text=f"Arlo arlo {utils.get_user(message)}. Use /add to start logging your expenses!")

@bot.message_handler(commands=['add'])
def add_transaction(message):
    userId = str(message.from_user.id)
    if userId not in allowed_users:
        text = "Sorry, you are not authorised for this command!!"
        bot.send_message(message.chat.id, text)
    else:
        sent_message = bot.send_message(chat_id=utils.get_chat_id(message), text="How much did you spend?")
        bot.register_next_step_handler(sent_message, set_amount_prompt_category)

def set_amount_prompt_category(message):
    try:
        amount = float(message.text)
        transaction = Transaction(amount, None, "", None, None)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for category in expense_categories:
            markup.add(category)
        sent_message = bot.send_message(chat_id=utils.get_chat_id(message), text="Ok. What category is it?", reply_markup=markup)
        bot.register_next_step_handler(sent_message, set_category_prompt_person, transaction)
    except ValueError:
        sent_message = bot.send_message(chat_id=utils.get_chat_id(message), text="Please check your input, ensure it is a number!")
        add_transaction(sent_message)

def set_category_prompt_person(message, transaction):
    transaction.category = message.text
    markup = ReplyKeyboardRemove()
    sent_message = bot.send_message(chat_id=utils.get_chat_id(message), text="Ok! Who spent this?", reply_markup = markup)

if __name__ == "__main__":
    bot.infinity_polling()