import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import random
import datetime

owner_id = 5395510109
# owner_id = 1809626375
# next_day = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
# extra_msg = "Please submit full information, note if you do not know your serial number or cert number leave blank."


def register_handlers(bot):
    bot.message_handler(func=lambda message: message.text == 'School Cert - K25')(lambda message: school_certificate_handler(bot, message))

def school_certificate_handler(bot, message):
    bot.reply_to(message, "You've chosen the School Certificates service. Please provide the following details.\n\n"
                          "🔸 Enter Full Name:")
    
    bot.register_next_step_handler(message, get_full_name, bot)

def get_full_name(message, bot):
    full_name = message.text
    bot.reply_to(message, "🏫 Enter Name of School:")
    bot.register_next_step_handler(message, get_school_name, bot, full_name)

def get_school_name(message, bot, full_name):
    school_name = message.text
    bot.reply_to(message, "📚 Select Grade Level:")
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("1. Grade 12", "2. Grade 10")
    bot.reply_to(message, "Select Grade Level:", reply_markup=keyboard)
    bot.register_next_step_handler(message, get_grade_level, bot, full_name, school_name)

def get_grade_level(message, bot, full_name, school_name):
    grade_level = message.text
    bot.reply_to(message, "📅 Enter Year Graduated (yyyy):")
    bot.register_next_step_handler(message, get_year_graduated, bot, full_name, school_name, grade_level)

def get_year_graduated(message, bot, full_name, school_name, grade_level):
    year_graduated = message.text
    bot.reply_to(message, "📚 Enter Subjects Taken and Grades. Include Changes as well\n\n (Separate each subject and grade by a comma):\n"
                          "Example: Math C Change to B, L&L B Change To A, And so on...")
    bot.register_next_step_handler(message, get_subjects_and_grades, bot, full_name, school_name, grade_level, year_graduated)

def get_subjects_and_grades(message, bot, full_name, school_name, grade_level, year_graduated):
    subjects_and_grades = message.text
    bot.reply_to(message, "🔢 Enter Serial Number:")
    bot.register_next_step_handler(message, get_serial_number, bot, full_name, school_name, grade_level, year_graduated, subjects_and_grades)

def get_serial_number(message, bot, full_name, school_name, grade_level, year_graduated, subjects_and_grades):
    serial_number = message.text
    bot.reply_to(message, "🎓 Enter Certificate Number:")
    bot.register_next_step_handler(message, get_certificate_number, bot, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number)

def get_certificate_number(message, bot, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number):
    certificate_number = message.text
    bot.reply_to(message, "📧 Enter Email Address\n\n🔸 (john.doe@example.com)")
    bot.register_next_step_handler(message, finish_handler, bot, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number, certificate_number)

def finish_handler(message, bot, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number, certificate_number):
    # Generate a unique 6-digit application ID number.
    application_id = generate_application_id()

    # Now, you can use all the collected information to create the cover letter or store it in a database, etc.
    # For this example, we'll simply notify the bot owner about the cover letter application.
    application_text = f"{message.from_user.first_name} (@{message.from_user.username}) has submitted a School Cert Application.\n\n" \
                       f"Details:\n🔰 Full Name: {full_name}\n🔰 Name of School: {school_name}\n🔰 Grade Level: {grade_level}\n" \
                       f"🔰 Year Graduated: {year_graduated}\n🔰 Subjects Taken and Grades: {subjects_and_grades}\n" \
                       f"🔰 Serial Number: {serial_number}\n🔰 Certificate Number: {certificate_number}\n\n🔰 Application ID: {application_id}"

    # Append the submission date and application ID to the application text.
    submission_date = datetime.datetime.now().strftime('%d-%m-%Y || %H:%M')
    application_text += f"\n\n📩 Submission Date:\{submission_date}"

    # Now, we'll ask the user if they want to submit the information using custom keyboard buttons.
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("✅ Yes", "❌ Cancel")
    bot.reply_to(message, "❔ Do you want to submit now?", reply_markup=keyboard)

    # Register a next step handler to handle the user's response.
    bot.register_next_step_handler(message, lambda msg: process_submission(bot, msg, application_text, application_id))

def process_submission(bot, message, application_text, application_id):
    if message.text.lower() == "✅ yes":
        # Get the current date and time for the submission.
        submission_date = datetime.datetime.now().strftime('%d-%m-%Y || %H:%M')

        # Notify the user about the successful submission and provide the application ID.
        bot.reply_to(message, f"Your School Cert application has been submitted on:\n{submission_date}. \n\n🔰 Your Application ID: {application_id}\n\n❗ Use this number to follow up on your application.\n\n❗ When following up you will be asked for your Application ID.\n\n❗ This will identify your application in the system. DO NOT submit the same application multiple times.\n\n❗ Follow up on submission via:\n🔸 @TheTypistBot or \n🔸 thetypisthelp@gmail.com.\n\nVisit our website: https://thetypist.epizy.com\n\nBack To Menu > /menu ",
                     reply_markup=ReplyKeyboardRemove())

        # Send the application details to the bot owner (same as before).
        bot.send_message(owner_id, application_text)  # Replace 'YOUR_OWNER_CHAT_ID' with the actual chat ID of the bot owner.

        # Save the information to the MySQL database (if desired).
        # save_to_database(application_id, application_text)
    else:
        # If the user chooses not to submit, provide a confirmation message.
        bot.reply_to(message, "❗❗ Your cover letter application has not been submitted.",
                     reply_markup=ReplyKeyboardRemove())

def generate_application_id():
    return str(random.randint(100000, 999999))
