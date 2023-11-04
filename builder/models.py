from django.db import models
from django.db.models import SET_NULL
from django.utils.datetime_safe import datetime

from extended_user.models import Profile
from graph_theory.settings import MEDIA_URL


# Create your models here.

class Graph(models.Model):
    name = models.CharField(max_length=1024, null=True, verbose_name='Название')
    creator = models.ForeignKey(to=Profile, on_delete=SET_NULL, null=True, related_name='graphs_by_creator',
                                verbose_name='Автор')
    time_create = models.DateTimeField(default=datetime.now, blank=True, verbose_name='Время создания')
    initial_data = models.TextField()
    graph_html = models.FileField()
    directed = models.BooleanField(default=False, verbose_name='Ориентированный граф')
    nodes_count = models.IntegerField(default=0, verbose_name='Количество вершин')

    @property
    def get_absolute_file_upload_url(self):
        return self.graph_html.name

    def __str__(self):
        return f"{self.name} (вершин: {self.nodes_count}, {self.creator})"
