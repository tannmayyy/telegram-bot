import os
import telebot
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv('')

# Initialize the bot with the token
bot = telebot.TeleBot('')

# Function to get daily horoscope from API
def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)
    return response.json()

# Handler for /start and /hello commands
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

# Command handler for /horoscope
@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer*, *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

# Handler for asking the day (today, tomorrow, etc.)
def day_handler(message):
    sign = message.text.strip().capitalize()
    
    # Check if the user entered a valid zodiac sign
    valid_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    if sign not in valid_signs:
        bot.send_message(message.chat.id, "Please enter a valid zodiac sign.")
        return
    
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign)

# Fetch horoscope and send to user
def fetch_horoscope(message, sign):
    day = message.text.strip().upper()

    # Check if the day is valid
    valid_days = ['TODAY', 'TOMORROW', 'YESTERDAY']
    if day not in valid_days and not day.isdigit():
        bot.send_message(message.chat.id, "Please enter a valid day (TODAY, TOMORROW, YESTERDAY, or YYYY-MM-DD).")
        return

    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")

# Start the bot's polling loop
bot.infinity_polling()
