import telebot
from telebot import types
import datetime
from config.secrets import BOT_TOKEN, ALLOWED_USERS
from config.bot_config import DATE_FORMAT
from bot.utils import months_day_map
from bot.transaction import Transaction
from bot.budget_manager import BudgetManager
from config.logging_config import logger
import bot.message_formatter as message_formatter

bot = telebot.TeleBot(BOT_TOKEN)
bm = BudgetManager()

bot.set_my_commands([
    types.BotCommand("/start", "To receive starting instructions"),
    types.BotCommand("/log", "To start logging transactions"),
    types.BotCommand("/list_months_transactions", "To list the transactions of the month"),
    types.BotCommand("/breakdown_by_month", "To get a breakdown of money spent on each category")
])

@bot.message_handler(commands=['start'])
def start(message):
    from_user = message.from_user
    chat = message.chat
    if str(from_user.id) in ALLOWED_USERS.keys():
        bot.send_message(chat.id, text=f"Hello {from_user.first_name}. Please use /log to log an expense. Other commands you can use are:")
    else:
        print("NOT AUTHORISED")

@bot.message_handler(commands=['log'])
def log(message):
    from_user = message.from_user
    chat = message.chat
    logger.info(f"bot_logger: /log called by {from_user.first_name}")
    if str(from_user.id) in ALLOWED_USERS.keys():
        text = "How much was spent?"
        markup = types.ReplyKeyboardRemove()
        sent_message = bot.send_message(chat.id, text=text, reply_markup=markup)
        bot.register_next_step_handler(sent_message, register_amount_prompt_person)
    else:
        print("NOT AUTHORISED")

def register_amount_prompt_person(message):
    chat = message.chat
    try:
        amount = float(message.text)
        transaction = Transaction(amount=amount)
        text = f"Ok, ${amount:.2f} was spent. Who spent it? Wens or Tians?"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Tians", "Wens", row_width=2)
        sent_message = bot.send_message(chat.id, text=text, reply_markup=markup)
        bot.register_next_step_handler(message=sent_message, callback=register_person_prompt_shared, transaction=transaction)
    except ValueError:
        pass

def register_person_prompt_shared(message, **kwargs):
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
        markup.add("Yes", "No", row_width=2)
        text = f"OK. Is it a shared transaction?"
        sent_message = bot.send_message(chat.id, text=text, reply_markup=markup)
        bot.register_next_step_handler(message=sent_message, callback=handle_shared_yes_no_prompt_category, transaction=transaction)

def handle_today_yes_no(message, **kwargs):
    chat = message.chat
    answer = message.text
    transaction = kwargs['transaction']
    date = datetime.datetime.now().strftime(DATE_FORMAT)
    if answer == "Yes":
        transaction.date = date
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("No comments!")
        text = "OK. Please leave your comments about this transaction. Press 'No comments!' if you don't have any."
        sent_message = bot.send_message(chat.id, text=text, reply_markup=markup)
        bot.register_next_step_handler(message=sent_message, callback=handle_comments_prompt_consolidate, transaction=transaction)
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
    bot.register_next_step_handler(message=sent_message, callback=handle_year_prompt_comments, transaction=transaction, day=day, month=month)

def handle_year_prompt_comments(message, **kwargs):
    chat = message.chat
    year = message.text
    month = kwargs['month']
    day = kwargs['day']
    transaction = kwargs['transaction']
    transaction.date = f"{day}-{month}-{year}"
    print(transaction.date)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("No comments!")
    text = "OK. Please leave your comments about this transaction. Press 'No comments!' if you don't have any."
    sent_message = bot.send_message(chat.id, text=text, reply_markup=markup)
    bot.register_next_step_handler(message=sent_message, callback=handle_comments_prompt_consolidate, transaction=transaction)

def handle_comments_prompt_consolidate(message, **kwargs):
    answer = message.text
    transaction = kwargs['transaction']
    if answer != "No comments!":
        transaction.description = answer
    text = f"""Ok. Please check your transaction:
        Amount: ${transaction.amount:.2f}
        Person: {transaction.person}
        Category: {transaction.category}
        Date: {transaction.date}
        Description: {transaction.description}
        Shared: {"Yes" if transaction.shared else "No"}
        """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Save!", "Abort!", row_width=2)
    sent_message = bot.send_message(message.chat.id, text=text, reply_markup=markup)
    bot.register_next_step_handler(message=sent_message, callback=handle_save_or_abort, transaction=transaction)

def handle_save_or_abort(message, **kwargs):
    transaction = kwargs['transaction']
    choice = message.text
    if choice == "Save!":
        text = "Ok saving transaction..."
        bm.save_transaction(transaction)
    else:
        text ="Ok aborting..."
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text=text, reply_markup=markup)

def handle_shared_yes_no_prompt_category(message, **kwargs):
    answer = message.text.lower()
    transaction = kwargs['transaction']
    transaction.shared = answer == "yes"
    text = "Sure! Which category does this expense belong to?"
    categories = bm.get_all_categories()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(*[category['name'] for category in categories], row_width=2)
    markup.add("Add new category")
    sent_message = bot.send_message(message.chat.id, text=text, reply_markup=markup)
    bot.register_next_step_handler(message=sent_message, callback=handle_category_response_prompt_date, transaction=transaction, categories=categories)

def handle_category_response_prompt_date(message, **kwargs):
    answer = message.text
    transaction = kwargs['transaction']
    categories = kwargs['categories']
    if answer == "Add new category":
        text = f"Ok, what is the new category?"
        sent_message = bot.send_message(message.chat.id, text=text)
        bot.register_next_step_handler(message=sent_message, callback=handle_add_new_category_prompt_date, transaction=transaction, categories=categories)
    else:
        transaction.category = answer
        text = "Roger that! Was it spent today?"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Yes", "No", row_width=2)
        sent_message = bot.send_message(message.chat.id, text=text, reply_markup=markup)
        bot.register_next_step_handler(message=sent_message, callback=handle_today_yes_no, transaction=transaction)

def handle_add_new_category_prompt_date(message, **kwargs):
    new_category = message.text
    transaction = kwargs['transaction']
    categories = kwargs['categories']
    categories_list = [category['name'] for category in kwargs['categories']]
    if new_category in categories_list:
        text = "This category already exists la. What you trying to do? Please enter a new category."
        sent_message = bot.send_message(message.chat.id, text=text)
        bot.register_next_step_handler(message=sent_message, callback=handle_add_new_category_prompt_date, transaction=transaction, categories=categories)
    else:
        bm.add_new_category(new_category)
        transaction.category = new_category
        text = f"Done! I have also added '{new_category}' to the list of categories that can be chosen.\nDid the transaction happen today?"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Yes", "No", row_width=2)
        sent_message = bot.send_message(message.chat.id, text=text, reply_markup=markup)
        bot.register_next_step_handler(message=sent_message, callback=handle_today_yes_no, transaction=transaction)

@bot.message_handler(commands=['list_months_transactions'])
def list_transactions_for_month(message):
    transactions = bm.get_current_months_transactions()
    # print(generate_message_table(transactions))

@bot.message_handler(commands=['breakdown_by_month'])
def get_breakdown_of_month(message):
    from_user = message.from_user
    id = from_user.id
    if str(id) in ALLOWED_USERS.keys():
        breakdown = bm.get_current_months_breakdown_by_id(id)
        text = "Ok. Here is the breakdown for the current month:\n"
        text += message_formatter.format_breakdown_message(breakdown)
        bot.send_message(message.chat.id, text=text, parse_mode="Markdown")
    else:
        print("NOT AUTHORISED")

if __name__ == "__main__":
    logger.info("Starting bot.")
    bot.infinity_polling()