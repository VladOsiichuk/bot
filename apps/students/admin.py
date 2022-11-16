from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm, CharField

from apps.students.models import Student, Course


class CourseForm(ModelForm):
    letter = CharField(required=False)

    class Meta:
        model = Course
        fields = "__all__"


class CourseAdmin(ModelAdmin):
    form = CourseForm


admin.site.register(Student)
admin.site.register(Course, CourseAdmin)