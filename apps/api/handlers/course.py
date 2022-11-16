from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.api.bot import bot
from apps.students.models import Course, Student


def set_course_callback_handler(callback):
    student = Student.objects.get(chat_id=callback.from_user.id)
    student.course_id = callback.data
    student.save()
    bot.send_message(student.chat_id, "Дякую. Тепер ти отримуватимеш інформацію по заняттях.")


def set_course(chat_id):
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(text=str(course), callback_data=str(course.id)) for course in Course.objects.all()]
    keyboard.add(*buttons)
    bot.send_message(chat_id, "Будь ласка, обери свій клас.", reply_markup=keyboard)
    handlers_dict = {
        "function": set_course_callback_handler,
        "filters": {}
    }
    bot.add_callback_query_handler(handlers_dict)


def set_course_handler(message):
    set_course(message.chat.id)
