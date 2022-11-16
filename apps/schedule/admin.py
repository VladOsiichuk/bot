from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline

from apps.schedule.forms import ScheduleLessonForm
from apps.schedule.models import ScheduleLesson, Schedule, ScheduleMaterial


class LessonMaterialInline(TabularInline):
    model = ScheduleMaterial


class ScheduleLessonAdmin(ModelAdmin):
    form = ScheduleLessonForm
    inlines = [LessonMaterialInline]


class ScheduleLessonInline(TabularInline):
    model = ScheduleLesson

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("ordering")

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ScheduleAdmin(ModelAdmin):
    inlines = [ScheduleLessonInline]


admin.site.register(ScheduleLesson, ScheduleLessonAdmin)
admin.site.register(Schedule, ScheduleAdmin)
