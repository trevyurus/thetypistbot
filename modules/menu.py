from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from modules import cv_cover_letter, police_clearance, school_cert, transcripts, help

def menu_handler(bot, message):
    # create menu keyboard
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Police Clearance K10')
    button2 = KeyboardButton('School Cert. - K25')
    button3 = KeyboardButton('CV & Cover Letter - K10')
    button4 = KeyboardButton('Transcripts - K25')
    button5 = KeyboardButton('Have another question?')
    faq_button = KeyboardButton('FAQs')
    keyboard.add(button1, button2)
    keyboard.add(button3, button4)
    keyboard.add(button5)

    # send menu message
    bot.reply_to(message, "Here are the services we offer:", reply_markup=keyboard)

    # register police clearance handlers
    police_clearance.register_handlers(bot)

    # register school cert handlers
    school_cert.register_handlers(bot)

    # register cover letter handlers
    cv_cover_letter.register_handlers(bot)

    # register cover transcripts handlers
    transcripts.register_handlers(bot)

    # register cover transcripts handlers
    help.register_handlers(bot)

    # Handle Button 5 ("Have another question?")
    @bot.message_handler(func=lambda message: message.text == 'Have another question?')
    def handle_help_request(message):
        help.help_handler(bot, message)

    # register other help handlers from the help.py file
    help.register_handlers(bot)

def register_handlers(bot):
    bot.message_handler(commands=['menu'])(lambda message: menu_handler(bot, message))
