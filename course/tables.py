import django_tables2 as tables
from course.models import Course, Lesson


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
