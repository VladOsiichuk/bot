from django.forms import ModelForm, fields

from apps.schedule.models import ScheduleLesson


class ScheduleLessonForm(ModelForm):
    start_at = fields.DateTimeField(required=False)

    class Meta:
        model = ScheduleLesson
        fields = "__all__"
