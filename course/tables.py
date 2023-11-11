import django_tables2 as tables
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

    class Meta:
        model = Task
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', 'name', 'weight', 'answer_count')


class HomeWorkTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'homework-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="", attrs={"tf": {"bgcolor": "red"}})

    class Meta:
        model = HomeWork
        template_name = "django_tables2/bootstrap5.html"
        fields = ('details', 'name', 'mark')
        # row_attrs = {
        #     'background-color': lambda record: '#f2dede' if record.mark is None else '008000'
        # }

        row_attrs = {
            'style': lambda record: f"""background:{record.table_color}"""
        }
