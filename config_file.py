""" Config file that holds all the values to run the bot

Values
------
bot_token: str
    The telegram bot token
db_file: str
    Name of the json database file

reactions: <str>:list
    A list of possible reactions to the poop message
"""

class config_class():
    def __init__(self):
        pass
config = config_class()

# Telegram bot ID
config.bot_token = ""

# Database in json format
config.db_file = "db.json"

# Reactions tot he poop message
config.reactions = [
    "❤️", 
    "🦄", 
    "💪",
]