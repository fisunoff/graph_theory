import itertools

import django_tables2 as tables
from django.utils.safestring import mark_safe

from course.models import Course, Lesson, Step, Task, HomeWork


class CourseTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'course-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="")

    class Meta:
        model = Course
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', "name",)


class LessonTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'lesson-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="")

    class Meta:
        model = Lesson
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', 'name',)


class StepTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'step-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="")

    class Meta:
        model = Step
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', 'name',)


class TaskTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'task-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="")

    answer_count = tables.Column(orderable=False, verbose_name="Решения")
    best = tables.Column(orderable=False, verbose_name="Лучшее решение", empty_values=())

    class Meta:
        model = Task
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', 'name', 'weight', 'max_mark', 'answer_count', 'best')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_best(self, value, record):
        if self.request.user.is_authenticated:
            values = record.homeworks.filter(creator_id=self.request.user.profile.id).values_list('mark', flat=True)
            if values:
                max_value = max(values)
                if max_value == record.max_mark:
                    return mark_safe(f"<span style='color:green; font-weight: bold;'>{max_value or '–'}</span>")
                return max_value or '–'
            return "–"
        return "–"


class HomeWorkTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'homework-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="", attrs={"tf": {"bgcolor": "red"}})

    title = tables.Column(verbose_name="Решение", orderable=False)
    title_with_author = tables.Column(verbose_name="Решение", orderable=False)

    class Meta:
        model = HomeWork
        template_name = "django_tables2/bootstrap5.html"
        fields = ('details', 'title', 'title_with_author', 'mark')

        row_attrs = {
            'style': lambda record: f"""background:{record.table_color}"""
        }
