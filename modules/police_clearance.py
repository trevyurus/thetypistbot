## Bot API: 6216214795:AAGX5Gy0zbrGw53-xzGoGcO1l2tvCIBIpfU

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import datetime
import random
import mysql.connector
# from modules import config

# bot = telebot.TeleBot(config)

# OWNER_CHAT_ID = 5395510109
bot = telebot.TeleBot('6216214795:AAGX5Gy0zbrGw53-xzGoGcO1l2tvCIBIpfU')

def register_handlers(bot):
    bot.message_handler(func=lambda message: message.text == 'Police Clearance K10')(lambda message: police_clearance_handler(bot, message))

def police_clearance_handler(bot, message):
    bot.reply_to(message, "You've chosen the Police Clearance service. Please provide the following details.\n\n"
                          "🔸 Enter Full Name:")
    
    bot.register_next_step_handler(message, get_full_name, bot)

def get_full_name(message, bot):
    full_name = message.text
    bot.reply_to(message, "📅 Enter Date of Birth (dd/mm/yy):")
    bot.register_next_step_handler(message, get_date_of_birth, bot, full_name)

def get_date_of_birth(message, bot, full_name):
    date_of_birth = message.text
    bot.reply_to(message, "🏥 Enter Place of Birth (Hospital, Town, Province)\n\n🔸 Example: Port Moresby General Hospital, Port Moresby, NCD")
    bot.register_next_step_handler(message, get_place_of_birth, bot, full_name, date_of_birth)

def get_place_of_birth(message, bot, full_name, date_of_birth):
    place_of_birth = message.text
    bot.reply_to(message, "🔹 Enter Place of Origin. (Village, District, Province)\n\n🔸 Example: Hanuabada, Port Moresby, NCD")
    bot.register_next_step_handler(message, get_place_of_origin, bot, full_name, date_of_birth, place_of_birth)

def get_place_of_origin(message, bot, full_name, date_of_birth, place_of_birth):
    place_of_origin = message.text
    bot.reply_to(message, "🏡 Enter Current Place of Residence. (Suburb,Town, Province)\n\n🔸 Example: Gerehu Stage 1, Port Moresby, NCD")
    bot.register_next_step_handler(message, get_current_residence, bot, full_name, date_of_birth, place_of_birth, place_of_origin)

def get_current_residence(message, bot, full_name, date_of_birth, place_of_birth, place_of_origin):
    current_residence = message.text
    bot.reply_to(message, "🛂 Enter Passport Number (If you do not have one send 'None.')")
    bot.register_next_step_handler(message, get_passport_number, bot, full_name, date_of_birth, place_of_birth, place_of_origin, current_residence)

def get_passport_number(message, bot, full_name, date_of_birth, place_of_birth, place_of_origin, current_residence):
    passport_number = message.text
    bot.reply_to(message, "📧 Enter Email Address\n\n🔸 (john.doe@example.com)")
    bot.register_next_step_handler(message, finish_handler, bot, full_name, date_of_birth, place_of_birth, place_of_origin, current_residence, passport_number)

def finish_handler(message, bot, full_name, date_of_birth, place_of_birth, place_of_origin, current_residence, passport_number):
    # Generate a unique 6-digit application ID number.
    application_id = generate_application_id()

    # Now, you can use all the collected information to create the cover letter or store it in a database, etc.
    # For this example, we'll simply notify the bot owner about the cover letter application.
    application_text = f"{message.from_user.first_name} (@{message.from_user.username}) has submitted a Cover Letter Application.\n\n" \
                       f"Details:\n🔰 Full Name: {full_name}\n🔰 Date of Birth: {date_of_birth}\n🔰 Place of Birth: {place_of_birth}\n" \
                       f"🔰 Place of Origin: {place_of_origin}\n🔰 Current Place of Residence: {current_residence}\n" \
                       f"🔰 Passport Number: {passport_number}\n\n🔰 Application ID: {application_id}"

    # Append the submission date and application ID to the application text.
    submission_date = datetime.now().strftime('%d-%m-%Y || %H:%M')
    application_text += f"\n\n📩 Submission Date:\{submission_date}"

    # Now, we'll ask the user if they want to submit the information using custom keyboard buttons.
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("✅ Yes", "❌ Cancel")
    bot.reply_to(message, "❔ Do you want to submit now?", reply_markup=keyboard)

    # Register a next step handler to handle the user's response.
    bot.register_next_step_handler(message, lambda msg: process_submission(bot, msg, application_text, application_id))

from datetime import datetime

# ...

def process_submission(bot, message, application_text, application_id):
    if message.text.lower() == "✅ yes":
        # Get the current date and time for the submission.
        submission_date = datetime.now().strftime('%d-%m-%Y || %H:%M')

        # Notify the user about the successful submission and provide the application ID.
        bot.reply_to(message, f"Your cover letter application has been submitted on:\n{submission_date}. \n\nYour Application ID: {application_id}\n\nUse this number to follow up on your application.\n\nWhen following up you will be asked for your Application ID.\n\nThis will identify your application in the system. DO NOT submit the same application multiple times.\n\nFollow up on submission via @TheTypistBot or thetypisthelp@gmail.com.\n\nVisit our website: https://thetypist.epizy.com\n\nBack To Menu > /menu ",
                     reply_markup=ReplyKeyboardRemove())

        # Send the application details to the bot owner (same as before).
        bot.send_message('5395510109', application_text)

        # Save the information to the MySQL database.
        # save_to_database(application_id, application_text)
    else:
        # If the user chooses not to submit, provide a confirmation message.
        bot.reply_to(message, "❗❗ Your cover letter application has not been submitted.",
                     reply_markup=ReplyKeyboardRemove())



def generate_application_id():
    return str(random.randint(100000, 999999))

# def save_to_database(full_name, current_address, email_address, application_id):
#     # Replace the database connection details with your actual MySQL database credentials.
#     db_config = {
#         'host': 'sql204.infinityfree.com',
#         'user': 'if0_34589154',
#         'password': 'arFPWj0qmPJm6I',
#         'database': 'if0_34589154_customers'  # The database name where the 'Cover Letter' table is located.
#     }

#     try:
#         # Establish a connection to the database. 
#         connection = mysql.connector.connect(**db_config)

#         # Create a cursor object to execute SQL queries.
#         cursor = connection.cursor()

#         # Prepare the SQL query to insert the data into the 'Cover Letter' table.
#         sql_query = "INSERT INTO cover_letters (`full name`, `current address`, `email`, `application id`) " \
#                     "VALUES (%s, %s, %s, %s)"

#         # Execute the query with the data provided.
#         cursor.execute(sql_query, (full_name, current_address, email_address, application_id))

#         # Commit the changes to the database.
#         connection.commit()

#         # Close the cursor and connection.
#         cursor.close()
#         connection.close()

#         print("Data saved to the database successfully.")
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
