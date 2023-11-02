import django_tables2 as tables

from builder.models import Graph


class GraphTable(tables.Table):
    details = tables.TemplateColumn('<a href="{% url \'graph-detail\' record.id %}">&#128203;</a>',
                                    orderable=False, verbose_name="")

    class Meta:
        model = Graph
        template_name = "django_tables2/bootstrap.html"
        fields = ('details', 'name', 'nodes_count', 'creator')
