import telebot
from modules import menu

# replace <YOUR_BOT_TOKEN> with your actual bot token obtained from BotFather
bot = telebot.TeleBot('5813832347:AAHp2cFngU_BUnbCATBRmI4MMIyM-8pmRMQ')

@bot.message_handler(commands=['start'])
def send_greeting(message):
    bot.reply_to(message, "Hello There!\n\nI'm The Typist Bot. You can submit your applications here.\n\nPlease take note of Priceing:\n\n🔰 Police Clearance - K10.00\n🔰 Cover Letter/CV - K10.00 (Letter Free)\n🔰 High School Certificates - K25.00\n\nYou can also visit our website\nhttps://thetypist.epizy.com/service\nto submit your applications\n\nPress >> /menu to see services.")

menu.register_handlers(bot)

bot.polling()
