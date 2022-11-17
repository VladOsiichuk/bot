from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from apps.schedule.forms import ScheduleLessonForm
from apps.schedule.models import ScheduleLesson, Schedule, ScheduleMaterial


class LessonMaterialInline(TabularInline):
    model = ScheduleMaterial


class ScheduleLessonAdmin(ModelAdmin):
    form = ScheduleLessonForm
    inlines = [LessonMaterialInline]

    list_filter = ("schedule__course",)


class ScheduleLessonInline(TabularInline):
    model = ScheduleLesson

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("ordering")


class ScheduleAdmin(ModelAdmin):
    inlines = [ScheduleLessonInline]
    list_filter = ("course",)

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("course__number", "day__date")


admin.site.register(ScheduleLesson, ScheduleLessonAdmin)
admin.site.register(Schedule, ScheduleAdmin)
