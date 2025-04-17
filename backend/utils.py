
def get_chat_id(message):
    return message.chat.id

def get_user(message):
    return message.from_user.first_name