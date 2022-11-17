from datetime import datetime, timedelta

from apps.api.bot import bot
from apps.schedule.models import Schedule, ScheduleLesson, ScheduleMaterial
from apps.students.models import Student
from config.celery import app


@app.task
def send_lesson_information(lesson_id):
    schedule_lesson = ScheduleLesson.objects.get(id=lesson_id)
    if not schedule_lesson.materials.all():
        return

    students = Student.objects.filter(course_id=schedule_lesson.schedule.course_id)
    for student in students:
        message = f"Розпочинається урок {schedule_lesson.lesson}. Матеріали до уроку: "
        bot.send_message(student.chat_id, message)
        for material in schedule_lesson.materials.all():
            if material.type == ScheduleMaterial.MaterialTypes.TASK:
                message = "Завдання"
            elif material.type == ScheduleMaterial.MaterialTypes.COMPENDIUM:
                message = "Конспект"
            else:
                message = "Контрольна робота"
            bot.send_message(student.chat_id, message)
            bot.send_document(student.chat_id, material.file)


@app.task
def schedule_lessons_for_today():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    schedules = Schedule.objects.filter(day__date__gte=today, day__date__lt=tomorrow)
    for schedule in schedules:
        for lesson in schedule.lessons.all():
            print(f"Scheduling lesson {lesson.id}. eta={lesson.start_at}")
            send_lesson_information.apply_async(eta=lesson.start_at, args=(lesson.id, ))

