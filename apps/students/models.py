from django.db import models


class Course(models.Model):
    number = models.PositiveSmallIntegerField()
    letter = models.CharField(max_length=1, default=None, null=True)

    def __str__(self):
        res = str(self.number)
        if self.letter:
            res += self.letter
        return res + " клас"


class Student(models.Model):
    course = models.ForeignKey(Course, null=True, default=None, on_delete=models.PROTECT, related_name="students")
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    chat_id = models.CharField(max_length=128)

    def __str__(self):
        name = f"{self.first_name} {self.last_name}"
        if self.course:
            name += f", {self.course}"
        return name
