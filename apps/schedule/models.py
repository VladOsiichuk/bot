from datetime import timedelta

from django.db import models
from django.utils.timezone import make_aware, make_naive

from apps.lessons.models import Lesson
from apps.students.models import Course


class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="schedule_days")
    day = models.DateTimeField()

    def __str__(self):
        return f"{self.day.date()} - {self.course}"


class ScheduleLesson(models.Model):
    ordering = models.PositiveSmallIntegerField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="lessons")
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, related_name="scheduled_days")

    duration_minutes = models.PositiveSmallIntegerField()
    break_after = models.PositiveSmallIntegerField()

    start_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.start_at:
            self._set_start_at()
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ("ordering", "schedule")

    def _set_start_at(self):
        other_lessons = ScheduleLesson.objects.filter(schedule_id=self.schedule_id, ordering__lt=self.ordering)
        initial_start = self.schedule.day

        for lesson in other_lessons:
            initial_start += timedelta(minutes=lesson.duration_minutes + lesson.break_after)
        self.start_at = initial_start

    def __str__(self):
        start_at = make_naive(self.start_at)
        start_at = start_at.strftime("%d-%m %H:%M")
        return f"{start_at}, {self.schedule.course}"


def _get_upload_to(instance, filename):
    return f"media/{instance.lesson_id}/{filename}"


class ScheduleMaterial(models.Model):
    class MaterialTypes(models.TextChoices):
        TEST = "TEST", "Test"
        COMPENDIUM = "COMPENDIUM", "Compendium"
        TASK = "TASK", "Task"

    lesson = models.ForeignKey(ScheduleLesson, on_delete=models.CASCADE, related_name="materials")
    type = models.CharField(choices=MaterialTypes.choices, max_length=32)
    file = models.FileField(upload_to=_get_upload_to)
