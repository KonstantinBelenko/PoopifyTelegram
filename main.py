"""Poopify Telegram Bot

This is a fun little side project I made for me and my girlfriend, Angelina
It's purpose is to provide a funny way to communicate, through the "Poop" 
message and a subsequent emoji response from the other person. 

DATABASE
--------
It uses little json file as the database for bot users and their friends.
To manage the database - I wrote a class inside the ./db_manager.py file.

The manager can automatically add new users, add their friends, 
conduct "user exists" and "already friends" checks, and also
return users friends and users name, all by providing only the Telegram ID of said user.

""" 

import telebot, json
from telebot import types
from config_file import config
from db_manager import db_manager

# Tools
bot = telebot.TeleBot(config.bot_token, parse_mode=None)
manager = db_manager(config.db_file)

# Reply keyboards
main_markup = types.ReplyKeyboardMarkup(row_width=1)
main_markup.add(types.KeyboardButton("💩 Poop"), types.KeyboardButton("🦄 Add friends"), types.KeyboardButton("🌈 Your friends"))

start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
start_markup.add(types.KeyboardButton("✅"), types.KeyboardButton("☠️"))

# Program starts here...

@bot.message_handler(commands=['start'])
def start_command(msg):

    if not manager.check_if_exists(msg.from_user.id):
        bot.reply_to(msg, "💩 Hi! I'm poopify bot! Would you like to start?", reply_markup=start_markup)
        bot.register_next_step_handler(msg, accpet_or_deny_new_user)
    else:
        bot.reply_to(msg, f"💩 Hello {msg.from_user.first_name}! You're already registred!", reply_markup=main_markup)

def accpet_or_deny_new_user(msg):
    if msg.text == '✅':
        manager.add_user(msg.from_user.id, f"@{msg.from_user.username}")
        bot.reply_to(msg, f"💩 Nice to meet you {msg.from_user.first_name}! Have a wonderfull poop!", reply_markup=main_markup)
    else:
        bot.reply_to(msg, "💩☠️ You sure?")
        bot.register_next_step_handler(msg, accpet_or_deny_new_user)


@bot.message_handler(func=lambda x: x.text == "💩 Poop")
def poop(msg):
    """ This is the main function that send the poop message
    """
    
    friends_list = manager.get_friends(str(msg.from_user.id))

    if len(friends_list) == 0:
        bot.reply_to(msg, f"💩 You did not add any friends yet! \nTo add a friend - send me his poop ID!")
    else:
        for friend_object in friends_list:
            friend_id = list(friend_object.keys())[0]
            
            # Create a custon inline reply markup based on the config set reactions
            keys = []
            for reaction in config.reactions:
                keys.append(types.InlineKeyboardButton(
                        reaction, 
                        callback_data=f"{reaction}:{friend_id}?{msg.from_user.id}"
                    ))
            inline_markup = types.InlineKeyboardMarkup([keys], row_width=len(config.reactions))

            bot.send_message(friend_id, f"💩 {msg.from_user.first_name} @{msg.from_user.username} just pooped!", reply_markup=inline_markup)

        bot.send_message(msg.chat.id, "💩 Poop was sent!")


@bot.callback_query_handler(func=lambda x: True)
def reaction_callback(callback):
    data = callback.data
    msg = data[0:data.find(':')]
    from_user = data[data.find(':')+1: data.find('?')]
    to_user = data[data.find('?')+1:]

    from_user_name = manager.get_name(str(from_user))
    bot.send_message(to_user, f"{from_user_name} reacted: {msg}")
    bot.edit_message_reply_markup(int(from_user), callback.message.id, reply_markup=types.InlineKeyboardMarkup([]))


@bot.message_handler(func=lambda x: x.text == "🦄 Add friends")
def add_friends(msg):
    bot.reply_to(msg, f"💩 Send me your friends poop ID! \n💩 Your poop ID is: {msg.from_user.id} ")
    bot.register_next_step_handler(msg, register_friend)

def register_friend(msg):
    try:
        friend_id = int(msg.text)

        if friend_id == int(msg.from_user.id):
            bot.reply_to(msg, "💩 Sorry, you can't add yourself as a friend :(")
        elif not manager.check_if_exists(str(friend_id)):
            bot.reply_to(msg, "💩 Sorry, that user did not register yet :(")
        elif manager.check_if_friends(str(msg.from_user.id), friend_id):
            bot.reply_to(msg, "💩 You're already friends!")
        else:
            bot.reply_to(msg, "💩 Got it!")
            manager.add_friend(str(msg.from_user.id), friend_id)
            manager.add_friend(str(friend_id), int(msg.from_user.id))

    except Exception as e:
        bot.reply_to(msg, "💩 Sorry, something's wrong with the code :(")

@bot.message_handler(func=lambda x: x.text=="🌈 Your friends")
def friends_list(msg):
    friends_list = manager.get_friends(str(msg.from_user.id))

    message_text = "💩 Your friends list:"
    for i, friend in enumerate(friends_list):
        name = list(friend.items())[0][1]
        message_text += "\n {} {}".format(i+1, name)

    bot.send_message(msg.chat.id, message_text)

bot.polling()