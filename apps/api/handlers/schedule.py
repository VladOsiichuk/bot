from datetime import datetime, timedelta

from django.utils.timezone import make_naive

from apps.api.bot import bot
from apps.schedule.models import Schedule
from apps.students.models import Student

WEEK_MAP = {
    0: "Понеділок",
    1: "Вівторок",
    2: "Середа",
    3: "Четвер",
    4: "П'ятниця",
    5: "Субота",
    6: "Неділя"
}


def show_schedule_handler(message):
    student = Student.objects.get(chat_id=message.chat.id)
    current_weekday = datetime.now().weekday()
    week_start = (datetime.now() - timedelta(days=current_weekday)).replace(hour=0)
    week_end = week_start + timedelta(days=7)
    schedules = Schedule.objects.filter(day__gt=week_start, day__lt=week_end, course_id=student.course_id).order_by("day")
    message = ""
    for schedule in schedules:
        message += WEEK_MAP[schedule.day.weekday()]
        message += "\n\n"
        for lesson in schedule.lessons.all():
            lesson_start_string = make_naive(lesson.start_at).strftime("%H:%M")
            lesson_row = f"{lesson_start_string} {lesson.lesson.name}\n"
            message += lesson_row
        message += "\n"
    message = message or "На цей тиждень розклад невідомий."
    bot.send_message(student.chat_id, message)
