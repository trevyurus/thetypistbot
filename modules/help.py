def register_handlers(bot):
    bot.message_handler(func=lambda message: message.text == 'Have another question?')(lambda message: help_handler(bot, message))


def help_handler(bot, message):
    reply_text = (
        "Hi there, need help with something else? Our team is looking forward to hearing from you. "
        "Kindly send us a message via @TheTypistBot or email us at thetypisthelp@gmail.com.\n\n"
        "FAQs:\n\n"
        "1. How long does it take for an application to be processed?\n"
        "Normally, it takes a day, but that also depends on the number of applications.\n\n"
        "2. Do we do reprints?\n"
        "NO. We create softcopies from the official template. Reprinting can be done by you. "
        "We recommend reprinting with Hardpaper sold in large stationary stores like Theodist.\n\n"
        "3. Is our letter writing service Free?\n"
        "Yes, of course, we do not charge for writing letters.\n\n"
        "4. Where else can we be contacted?\n"
        "Facebook - https://www.facebook.com/thetypistbot\n"
        "Telegram Channel - https://t.me/thetypistb0t\n"
        "Applications Bot - https://t.me/thetypistapplications_bot\n"
        "Support Bot - https://t.me/TheTypistBot\n\n"
        ">> Back to /menu || Restart Bot /start"
    )

    bot.reply_to(message, reply_text)
