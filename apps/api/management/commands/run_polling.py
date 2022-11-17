from django.core.management import BaseCommand
from telebot.types import BotCommand

from apps.api.bot import bot
from apps.api.handlers.course import set_course_handler
from apps.api.handlers.schedule import show_schedule_handler
from apps.api.handlers.start import start_handler


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        print("Start bot")
        bot.set_my_commands(
            [
                BotCommand(command="/set_course", description="Змінити клас"),
                BotCommand(command="/show_schedule", description="Переглянути розклад")
            ]
        )
        start_handler_params = {
            "function": start_handler,
            "filters": {"commands": ["start"]}
        }
        bot.add_message_handler(start_handler_params)

        set_course_handler_params = {
            "function": set_course_handler,
            "filters": {"commands": ["set_course"]}
        }
        bot.add_message_handler(set_course_handler_params)
        show_schedule_handler_params = {
            "function": show_schedule_handler,
            "filters": {"commands": ["show_schedule"]}
        }
        bot.add_message_handler(show_schedule_handler_params)
        bot.polling(True)
