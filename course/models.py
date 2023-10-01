from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import SET_NULL, CASCADE
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from martor.models import MartorField

from extended_user.models import Profile


class BaseUnit:
    pass


class Course(BaseUnit, models.Model):
    name = models.CharField(max_length=1024, null=True)
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='courses_by_creator')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='courses_by_last_editor')
    time_create = models.DateTimeField(default=datetime.now, blank=True)
    time_edit = models.DateTimeField(default=datetime.now, blank=True)
    description = models.CharField(max_length=1024, default="Описание не заполнено")
    editors = models.ManyToManyField(to=Profile)
    private = models.BooleanField(default=False)
    password = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name or "Нет названия"

    def get_absolute_url(self):
        return reverse_lazy('course-detail', kwargs={'pk': self.pk})


class Lesson(BaseUnit, models.Model):
    name = models.CharField(max_length=1024, null=True)
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='lessons_by_creator')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='lessons_by_last_editor')
    time_create = models.DateTimeField(default=datetime.now, blank=True)
    time_edit = models.DateTimeField(default=datetime.now, blank=True)
    description = models.CharField(max_length=1024, default="Описание не заполнено")
    course = models.ForeignKey(to=Course, on_delete=CASCADE, related_name='lessons')

    def __str__(self):
        return self.name or "Нет названия"


class Step(BaseUnit, models.Model):  # шаги занятия
    name = models.CharField(max_length=1024, null=True)
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='steps_by_creator')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='steps_by_last_editor')
    time_create = models.DateTimeField(default=datetime.now, blank=True)
    time_edit = models.DateTimeField(default=datetime.now, blank=True)
    description = models.CharField(max_length=1024, default="Описание не заполнено")
    lesson = models.ForeignKey(to=Lesson, on_delete=CASCADE, related_name='steps')
    data = MartorField()

    def __str__(self):
        return self.name or "Нет названия"


class Task(BaseUnit, models.Model):  # в одном занятии может быть несколько заданий
    name = models.CharField(max_length=1024, null=True)
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='tasks_by_creator')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='tasks_by_last_editor')
    time_create = models.DateTimeField(default=datetime.now, blank=True)
    time_edit = models.DateTimeField(default=datetime.now, blank=True)
    description = models.CharField(max_length=1024, default="Описание не заполнено")
    step = models.ForeignKey(to=Step, on_delete=CASCADE, related_name='tasks')
    max_mark = models.IntegerField()
    weight = models.IntegerField(default=10)

    def __str__(self):
        return self.name or "Нет названия"


class HomeWork(BaseUnit, models.Model):
    name = models.CharField(max_length=1024, null=True)
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='homeworks_by_creator')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='homeworks_by_last_editor')
    time_create = models.DateTimeField(default=datetime.now, blank=True)
    time_edit = models.DateTimeField(default=datetime.now, blank=True)
    description = models.CharField(max_length=1024, default="Описание не заполнено")
    task = models.ForeignKey(to=Step, on_delete=SET_NULL, null=True, related_name='homeworks')
    mark = models.IntegerField()

    def __str__(self):
        return f"{self.name} пользователя {self.creator}"


class RegOnCourse(models.Model):
    intern = models.ForeignKey("extended_user.Profile", verbose_name="Студент", on_delete=models.RESTRICT,
                               related_name="regs_by_student")
    course_id = models.ForeignKey("Course", verbose_name="Курс", on_delete=models.RESTRICT,
                                  related_name="regs_by_course")
    rating = models.IntegerField("Обратная связь", null=True, blank=True, validators=[MinValueValidator(0),
                                                                                      MaxValueValidator(5)])
