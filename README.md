# 💩 Poopify Telegram Bot
Poopify telegram bot is just a little silly side project of mine that I dedicated for me and my girlfriend. <br/>
The premise is to communicate with your friends by sending the "poop" message to your friends thorugh the bot, and receiving their emoji reactions afterwards.

# ⚡️ How to install / run
**0. Download this library and cd into the library folder**
```
git clone https://github.com/KonstantinBelenko/PoopifyTelegram.git
cd PoopifyTelegram
```

**1. As the first step I recomend you to set up a virtual environment and download app dependencies.**
```
### Code povided here is present on Ubuntu 20.04 LTS

# 1. Install python3-pip
$ sudo apt-get install python3-pip

# 2. Install the virtualenv
$ sudo pip3 install virtualenv 

# 3. Create and activate the virtual environment
$ virtualenv venv 
$ source ./venv/bin/activate

# 4. Install dependencies
$ pip3 install -r requirements.txt
```

**2. Fill out the config_file.py**
1. config.bot_token needs to hold the token of the telegram bot you're going to use
2. config.db_file (default: "db.json") is optional. You can set the database file to be anything you want **(File needs to be created beforehand)**
3. config.reactions (optional). You can create which reactions your friends are going to be able to respond with.
**3. Run the bot**
1. Entry point for the program is main.py
```python
$ python3 main.py
```
**4. 🦄 Have fun 🌈**
