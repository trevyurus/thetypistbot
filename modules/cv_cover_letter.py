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
    bot.message_handler(func=lambda message: message.text == 'CV & Cover Letter - K10')(lambda message: cv_cover_letter_handler(bot, message))


def cv_cover_letter_handler(bot, message):
    bot.reply_to(message, "You've chosen the cover letter service. Please provide the following details.\n\n"
                          "🔸 Enter Full Name:")
    
    bot.register_next_step_handler(message, get_full_name, bot)

def get_full_name(message, bot):
    full_name = message.text
    bot.reply_to(message, "🏡 Enter Current Address.\n(PO Box, Street, Town, City):")
    bot.register_next_step_handler(message, get_current_address, bot, full_name)

def get_current_address(message, bot, full_name):
    current_address = message.text
    bot.reply_to(message, "📧 Enter Email Address. \n(john.doe@example.com):")
    bot.register_next_step_handler(message, get_email_address, bot, full_name, current_address)

def get_email_address(message, bot, full_name, current_address):
    email_address = message.text
    # Now we will ask whether the user is currently employed.
    # We'll use a custom keyboard with two buttons: "Yes" and "No".
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("✅ Yes", "❌ No")
    bot.reply_to(message, "Are you currently employed?\nChoose an answer:", reply_markup=keyboard)

    # We'll use a lambda function as the next step handler to handle the user's response for employment status.
    bot.register_next_step_handler(message, lambda msg: process_employment_status(bot, msg, full_name, current_address, email_address))

def process_employment_status(bot, message, full_name, current_address, email_address):
    employment_status = message.text.lower()
    
    if employment_status == "✅ yes":
        bot.reply_to(message, "🔸 Please provide the name of your current Employer (Company Name):")
        bot.register_next_step_handler(message, get_company_name, bot, full_name, current_address, email_address)
    else:
        # If the user is not employed, we proceed to collect other information.
        bot.reply_to(message, "🎓 Please provide your education history:\n\nInstitution | Certification | Year Graduated\n\n(Add as many as you need, on separate lines)")
        bot.register_next_step_handler(message, get_education_history, bot, full_name, current_address, email_address, None)

def get_company_name(message, bot, full_name, current_address, email_address):
    company_name = message.text
    bot.reply_to(message, "🎓 Please provide your education history:\n\nInstitution | Certification | Year Graduated\n\n(Add as many as you need, on separate lines)")
    bot.register_next_step_handler(message, get_education_history, bot, full_name, current_address, email_address, company_name)

def get_education_history(message, bot, full_name, current_address, email_address, company_name):
    education_history = message.text
    bot.reply_to(message, "🏢 Please provide your work history/experience:\n\nCompany | Position | Year\n\n(Add as many as you need, on separate lines)")
    bot.register_next_step_handler(message, get_work_history, bot, full_name, current_address, email_address, company_name, education_history)

def get_work_history(message, bot, full_name, current_address, email_address, company_name, education_history):
    work_history = message.text
    bot.reply_to(message, "🏆 Please provide any awards or achievements you'd like to include.\n\nList in following format\nAward| Date | Institution\nAward| Date | Institution\nAward| Date | Institution\n\nOn seprate lines. (If none, then send 'None.')")
    bot.register_next_step_handler(message, get_awards_achievements, bot, full_name, current_address, email_address, company_name, education_history, work_history)

def get_awards_achievements(message, bot, full_name, current_address, email_address, company_name, education_history, work_history):
    awards_achievements = message.text
    bot.reply_to(message, "📝 Enter the NAME and, POSITION of the company you are applying to:")
    bot.register_next_step_handler(message, get_company_applying_to, bot, full_name, current_address, email_address, company_name, education_history, work_history, awards_achievements)

def get_company_applying_to(message, bot, full_name, current_address, email_address, company_name, education_history, work_history, awards_achievements):
    company_applying_to = message.text
    bot.reply_to(message, "🏢 Enter the address (PO Box) of the company you are applying to:")
    bot.register_next_step_handler(message, finish_handler, bot, full_name, current_address, email_address, company_name, education_history, work_history, awards_achievements, company_applying_to)

def finish_handler(message, bot, full_name, current_address, email_address, company_name, education_history, work_history, awards_achievements, company_applying_to):
    # Now, you can use all the collected information to create the cover letter or store it in a database, etc.
    # For this example, we'll simply notify the bot owner about the cover letter application.
    application_text = f"{message.from_user.first_name} (@{message.from_user.username}) has submitted a Cover Letter Application.\n\n" \
                       f"Details:\nFull Name: {full_name}\nCurrent Address: {current_address}\nEmail Address: {email_address}\n" \
                       f"Employed: {'Yes' if company_name else 'No'}\n{'Company Name: ' + company_name if company_name else ''}\n" \
                       f"Education History: {education_history}\nWork History/Experience: {work_history}\n" \
                       f"Awards/Achievements: {awards_achievements}\nCompany Applying To: {company_applying_to}"

    # Now, we'll ask the user if they want to submit the information using custom keyboard buttons.
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("✅ Yes", "❌ Cancel")
    bot.reply_to(message, "Do you want to submit now?", reply_markup=keyboard)

    # Register a next step handler to handle the user's response.
    bot.register_next_step_handler(message, lambda msg: process_submission(bot, msg, full_name, current_address, email_address, company_name, education_history, work_history, awards_achievements, company_applying_to))



from datetime import datetime

# ...

def process_submission(bot, message, full_name, current_address, email_address, company_name, education_history, work_history, awards_achievements, company_applying_to):
    if message.text.lower() == "✅ yes":
        # If the user wants to submit, we'll generate a unique 6-digit application ID number.
        application_id = generate_application_id()

        # Get the current date and time for the submission.
        submission_date = datetime.now().strftime('%d-%m-%Y %H:%M')

        # Notify the user about the successful submission and provide the application ID.
        bot.reply_to(message, f"Your cover letter application has been submitted on: {submission_date}.\n\n🔰 Your Application ID: `{application_id}`\n\n❗ Use this number to follow up on your application.\n\n❗ When following up you will be asked for your App Number.\n\n❗ This will identify your application in the system. *Do not submit the same application multiple times*.\n\n❗ Follow up on application status via:\n🔸 @TheTypistBot or\n🔸 thetypisthelp@gmail.com\n\nVisit our website:\nhttps://thetypist.epizy.com\n\nBack To Menu > /menu ",
                     reply_markup=ReplyKeyboardRemove())

        # Send the application details to the bot owner (same as before).
        application_text = f"{message.from_user.first_name} (@{message.from_user.username}) has submitted a CV/Cover Letter Application.\n\n" \
                           f"🔰 Application ID: {application_id}\n🔰 Submission Date: {submission_date}\n\n🔸 Details:\n🔰 Full Name: {full_name}\n\n🔰 Current Address:\n{current_address}\n\n🔰 Email Address:\n{email_address}\n\n" \
                           f"🔰 Employed: {'Yes' if company_name else 'No'}\n{'🔰 Current Employer: ' + company_name if company_name else ''}\n\n" \
                           f"🔰 Education History:\n{education_history}\n\n🔰 Work History/Experience:\n{work_history}\n\n" \
                           f"🔰 Awards/Achievements:\n{awards_achievements}\n\n🔰 Company Applying To:\n{company_applying_to}"  

        # Send the message to the bot owner (you can replace '5395510109' with the bot owner's chat ID)
        bot.send_message('5395510109', application_text)
        

        # Save the information to the MySQL database.
        save_to_database(full_name, current_address, email_address, application_id)
    else:
        # If the user chooses not to submit, provide a confirmation message.
        bot.reply_to(message, "Your cover letter application has not been submitted.",
                     reply_markup=ReplyKeyboardRemove())


def generate_application_id():
    return str(random.randint(100000, 999999))

def save_to_database(full_name, current_address, email_address, application_id):
    # Replace the database connection details with your actual MySQL database credentials.
    db_config = {
        'host': 'sql204.infinityfree.com',
        'user': 'if0_34589154',
        'password': 'arFPWj0qmPJm6I',
        'database': 'if0_34589154_customers'  # The database name where the 'Cover Letter' table is located.
    }

    try:
        # Establish a connection to the database. 
        connection = mysql.connector.connect(**db_config)

        # Create a cursor object to execute SQL queries.
        cursor = connection.cursor()

        # Prepare the SQL query to insert the data into the 'Cover Letter' table.
        sql_query = "INSERT INTO cover_letters (`full name`, `current address`, `email`, `application id`) " \
                    "VALUES (%s, %s, %s, %s)"

        # Execute the query with the data provided.
        cursor.execute(sql_query, (full_name, current_address, email_address, application_id))

        # Commit the changes to the database.
        connection.commit()

        # Close the cursor and connection.
        cursor.close()
        connection.close()

        print("Data saved to the database successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
