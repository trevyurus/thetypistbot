import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import random
import datetime
import re

owner_id = 5395510109
# owner_id = 1809626375


def register_handlers(bot):
    bot.message_handler(func=lambda message: message.text == 'Transcripts - K25')(lambda message: transcripts_handler(bot, message))

def transcripts_handler(bot, message):
    application_id = generate_application_id()
    bot.reply_to(message, "You've chosen the **Transcripts** service. Please provide the following details.\n\n"
                          "🔸 Enter Full Name:")
    bot.register_next_step_handler(message, get_full_name, bot, application_id)

def get_full_name(message, bot, application_id):
    full_name = message.text
    bot.reply_to(message, "🏫 Enter Name of School/Institution:\n\n(Example: F.O.D.E)")
    bot.register_next_step_handler(message, get_school_name, bot, application_id, full_name)

def get_school_name(message, bot, application_id, full_name):
    school_name = message.text
    bot.reply_to(message, "🎓 Grade level Upgrading?\n\nPlease select one option:\n\nIf you're upgrading for grade 11 choose 'Other' and specify in a short brief explanation.", reply_markup=get_grade_level_keyboard())
    bot.register_next_step_handler(message, get_grade_level, bot, application_id, full_name, school_name)

def get_grade_level_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🔸 Grade 12", "🔸 Grade 10", "❔ Other")
    return keyboard

def get_grade_level(message, bot, application_id, full_name, school_name):
    grade_level = message.text
    if grade_level.lower() == "❔ other":
        bot.reply_to(message, "📝 Please provide a brief description:")
        bot.register_next_step_handler(message, get_grade_level_description, bot, application_id, full_name, school_name)
    else:
        bot.reply_to(message, "📅 Enter Year Graduated:")
        bot.register_next_step_handler(message, get_year_graduated, bot, application_id, full_name, school_name, grade_level)

def get_grade_level_description(message, bot, application_id, full_name, school_name):
    grade_level_description = message.text
    bot.reply_to(message, "📅 Enter Year Graduated:")
    bot.register_next_step_handler(message, get_year_graduated, bot, application_id, full_name, school_name, grade_level_description)

def get_year_graduated(message, bot, application_id, full_name, school_name, grade_level):
    year_graduated = message.text
    bot.reply_to(message, "📚 Enter Subjects taken and Grades To Upgrade/Change. One Entry on a new line.\n\nExample: \nMath C Change to B\n L&L B Change to A")
    bot.register_next_step_handler(message, get_subjects_and_grades, bot, application_id, full_name, school_name, grade_level, year_graduated)

def get_subjects_and_grades(message, bot, application_id, full_name, school_name, grade_level, year_graduated):
    subjects_and_grades = message.text
    bot.reply_to(message, "🔢 Enter Serial Number:\n\n(As seen on your original Certificate in format 20XX-G12-XXXXX.\n\nIf None then send 'None.')")
    bot.register_next_step_handler(message, get_serial_number, bot, application_id, full_name, school_name, grade_level, year_graduated, subjects_and_grades)

def get_serial_number(message, bot, application_id, full_name, school_name, grade_level, year_graduated, subjects_and_grades):
    serial_number = message.text
    bot.reply_to(message, "🔑 Enter Certificate Number.\n\nAs seen on your **original certificate** If unavailable then send 'None.'")
    bot.register_next_step_handler(message, get_certificate_number, bot, application_id, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number)

def get_certificate_number(message, bot, application_id, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number):
    certificate_number = message.text
    bot.reply_to(message, "📧 Enter Email Address (john.doe@example.com)\n\nFor delivery of your transcripts.")
    bot.register_next_step_handler(message, get_email_address, bot, application_id, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number, certificate_number)

def get_email_address(message, bot, application_id, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number, certificate_number):
    email_address = message.text
    bot.reply_to(message, "📄 Upload Scan of Transcript Scan (PDF format).\n\n❗❗Photo Submissions are low quality therefore bot will reject files if not PDF")
    bot.register_next_step_handler(message, process_file_upload, bot, application_id, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number, certificate_number, email_address)

def process_file_upload(message, bot, application_id, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number, certificate_number, email_address):
    if message.document is not None and message.document.mime_type == 'application/pdf':
        # Download the file
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'

        # Collect all user inputs
        submission_date = datetime.datetime.now().strftime('%d-%m-%Y || %H:%M')  # Define submission_date here
        application_text = f"Transcript Application Submitted by {message.from_user.first_name} (@{message.from_user.username})\n 🔰 Full Name: \n{full_name}\n\n🏫 School/Institution: \n{school_name}\n\n🎓 Grade Level Upgrading: \n{grade_level}\n\n📅 Year Graduated: \n{year_graduated}\n\n📚 Subjects and Grades To Upgraded/Changed: \n{subjects_and_grades}\n\n🔢 Serial Number: \n{serial_number}\n\n🔑 Certificate Number: \n{certificate_number}\n\n📧 Email Address: \n{email_address}\n\n📄 Transcript Scan: \n{file_url}\n\n🔰 Application ID: {application_id}\n📩 Submission Date: {submission_date}"

        # Notify the user about the successful submission and provide the application ID.
        bot.reply_to(message, f"Your Transcript application has been submitted on:\n{submission_date}. \n\n🔰 Your Application ID: {application_id}\n\n❗ Use this number to follow up on your application.\n\n❗ When following up, you will be asked for your Application ID.\n\n❗ This will identify your application in the system. DO NOT submit the same application multiple times.\n\n❗ Follow up on submission via \n🔸 @TheTypistBot or \n🔸 thetypisthelp@gmail.com.\n\n🔸 Visit our website: https://thetypist.epizy.com\n\nBack To Menu > /menu ",
                     reply_markup=ReplyKeyboardRemove())

        # Send the application details to the bot owner
        bot.send_message('5395510109', application_text)

        # Save the information to the MySQL database
        # save_to_database(full_name, email_address, application_id)

    else:
        bot.reply_to(message, "❗ Please upload a valid PDF file.")
        bot.register_next_step_handler(message, process_file_upload, bot, application_id, full_name, school_name, grade_level, year_graduated, subjects_and_grades, serial_number, certificate_number, email_address)

def generate_application_id():
    return str(random.randint(100000, 999999))
