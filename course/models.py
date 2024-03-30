from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import SET_NULL, CASCADE
from django.urls import reverse_lazy

from martor.models import MartorField

from builder.models import Graph
from extended_user.models import Profile


class BaseUnit:
    pass


class Course(BaseUnit, models.Model):
    name = models.CharField(max_length=1024, null=True, verbose_name='Название')
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='courses_by_creator',
                                verbose_name='Автор')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='courses_by_last_editor',
                                    verbose_name='Последний редактор')
    time_create = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Время создания')
    time_edit = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Последнее редактирование')
    description = models.TextField(max_length=4096, default="Описание не заполнено", verbose_name='Описание')
    editors = models.ManyToManyField(to=Profile, verbose_name='Редакторы')
    private = models.BooleanField(default=False, verbose_name='С ограниченным доступом')
    password = models.CharField(max_length=1024, blank=True, null=True, verbose_name='Пароль')

    def __str__(self):
        return self.name or "Нет названия"

    def get_absolute_url(self):
        return reverse_lazy('course-detail', kwargs={'pk': self.pk})

    def is_parent_creator(self, user_pk):
        raise NotImplementedError


class Lesson(BaseUnit, models.Model):
    name = models.CharField(max_length=1024, null=True, verbose_name='Название')
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='lessons_by_creator',
                                verbose_name='Автор')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='lessons_by_last_editor',
                                    verbose_name='Последний редактор')
    time_create = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Время создания')
    time_edit = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Последнее редактирование')
    description = models.TextField(max_length=4096, default="Описание не заполнено", verbose_name='Описание')
    course = models.ForeignKey(to=Course, on_delete=CASCADE, related_name='lessons', verbose_name='Курс')

    def __str__(self):
        return self.name or "Нет названия"

    def get_absolute_url(self):
        return reverse_lazy('lesson-detail', kwargs={'pk': self.pk})

    def is_parent_creator(self, user_pk):
        return self.creator_id == user_pk

    @property
    def parent(self):
        return self.course

    @classmethod
    def parent_class(cls):
        return Course


class Step(BaseUnit, models.Model):  # шаги занятия
    name = models.CharField(max_length=1024, null=True, verbose_name='Название')
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='steps_by_creator',
                                verbose_name='Автор')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='steps_by_last_editor',
                                    verbose_name='Последний редактор')
    time_create = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Время создания')
    time_edit = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Последнее редактирование')
    description = models.TextField(max_length=4096, default="Описание не заполнено", verbose_name='Описание')
    lesson = models.ForeignKey(to=Lesson, on_delete=CASCADE, related_name='steps', verbose_name='Занятие')
    data = MartorField(verbose_name='Материалы шага')
    graph = models.ForeignKey(to=Graph, null=True, blank=True, on_delete=SET_NULL, verbose_name='Иллюстрация к шагу')

    def __str__(self):
        return self.name or "Нет названия"

    def get_absolute_url(self):
        return reverse_lazy('step-detail', kwargs={'pk': self.pk})

    def is_parent_creator(self, user_pk):
        return self.creator_id == user_pk or self.parent.is_parent_creator(user_pk)

    @property
    def parent(self):
        return self.lesson

    @classmethod
    def parent_class(cls):
        return Lesson


class Task(BaseUnit, models.Model):  # в одном занятии может быть несколько заданий
    name = models.CharField(max_length=1024, null=True, verbose_name='Название')
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='tasks_by_creator',
                                verbose_name='Автор')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='tasks_by_last_editor',
                                    verbose_name='Последний редактор')
    time_create = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Время создания')
    time_edit = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Последнее редактирование')
    description = models.TextField(max_length=4096, default="Описание не заполнено", verbose_name='Описание')
    step = models.ForeignKey(to=Step, on_delete=CASCADE, related_name='tasks', verbose_name='Шаг')
    max_mark = models.IntegerField(verbose_name='Максимальная оценка')
    weight = models.IntegerField(default=10, verbose_name='Вес оценки')
    auto_test = models.BooleanField(verbose_name="Автоматическая проверка", default=False)
    correct_answers = models.TextField(verbose_name="Правильные ответы (варианты через ;)", null=True, blank=True)
    graph = models.ForeignKey(to=Graph, null=True, blank=True, on_delete=SET_NULL, verbose_name='Иллюстрация к заданию')

    def __str__(self):
        return self.name or "Нет названия"

    def get_absolute_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.pk})

    @property
    def answer_count(self):
        return self.homeworks.count()

    def is_parent_creator(self, user_pk):
        return self.creator_id == user_pk or self.parent.is_parent_creator(user_pk)

    @property
    def parent(self):
        return self.step

    @classmethod
    def parent_class(cls):
        return Step


class HomeWork(BaseUnit, models.Model):
    name = models.CharField(max_length=1024, null=True, verbose_name='Название', blank=True)
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='homeworks_by_creator',
                                verbose_name='Автор')
    last_editor = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='homeworks_by_last_editor',
                                    verbose_name='Проверяющий')
    time_create = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Время создания')
    time_edit = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Последнее редактирование')
    description = models.TextField(max_length=1024, verbose_name='Решение', null=True)
    task = models.ForeignKey(to=Task, on_delete=SET_NULL, null=True, related_name='homeworks', verbose_name='Задание')
    mark = models.IntegerField(verbose_name='Оценка', null=True, blank=True)

    @property
    def title(self):
        if len(self.description) > 50:
            return self.description[:50] + '...'
        return self.description

    @property
    def title_with_author(self):
        return f"{self.title} ({self.creator})"

    def __str__(self):
        return self.title_with_author

    def get_absolute_url(self):
        return reverse_lazy('homework-detail', kwargs={'pk': self.pk})

    def is_parent_creator(self, user_pk):
        return self.creator_id == user_pk or self.parent.is_parent_creator(user_pk)

    @property
    def table_color(self):
        if self.mark == self.task.max_mark:
            return 'green'
        if self.mark is None:
            return ''
        if self.mark == 0:
            return 'red'
        return 'yellow'

    @property
    def parent(self):
        return self.task

    @classmethod
    def parent_class(cls):
        return Task


class RegOnCourse(models.Model):
    intern = models.ForeignKey("extended_user.Profile", verbose_name="Студент", on_delete=models.RESTRICT,
                               related_name="regs_by_student")
    course_id = models.ForeignKey("Course", verbose_name="Курс", on_delete=models.RESTRICT,
                                  related_name="regs_by_course")
    rating = models.IntegerField("Обратная связь", null=True, blank=True, validators=[MinValueValidator(0),
                                                                                      MaxValueValidator(5)])
