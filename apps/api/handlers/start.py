from apps.api.bot import bot
from apps.api.handlers.course import set_course
from apps.students.models import Student


def start_handler(message):
    student, _ = Student.objects.update_or_create(
        chat_id=message.chat.id,
        defaults={
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
        }
    )

    if student.course:
        bot.send_message(student.chat_id, f"Чудово. тепер ти знову будеш отримувати сповіщення свого {student.course}у")
    else:
        set_course(student.chat_id)
