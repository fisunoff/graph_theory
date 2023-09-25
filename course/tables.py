import django_tables2 as tables
from course.models import Course


class CourseTable(tables.Table):
    # edit = tables.TemplateColumn('<a href="{% url \'reg_event-detail\' record.id %}">&#128203;</a>',
    #                              orderable=False, verbose_name="")

    class Meta:
        model = Course
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", )
