from django.core.files import File
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django_tables2 import SingleTableView

from builder.drawer import draw, DEFAULT_FILENAME, DEFAULT_PATH
from builder.models import Graph
from builder.tables import GraphTable
from course.views.mixins import AddTitleFormMixin, SaveEditorMixin


class GraphListView(SingleTableView):
    model = Graph
    template_name = 'builder/list.html'
    table_class = GraphTable

    def get_queryset(self):
        return self.model.objects.all()


class GraphCreateView(SaveEditorMixin, AddTitleFormMixin, CreateView):
    model = Graph
    template_name = 'base_create.html'
    save_creator_only = True

    fields = ('name', 'directed', 'initial_data')

    title = "Добавление урока"

    def get_success_url(self):
        return reverse_lazy('graph-detail', kwargs={'pk': self.object.id})

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
        return initial_data

    def process_file(self, input_data: str, directed: bool) -> int:
        """
        Генерация html файла с графом по входным данным
        :param input_data: Входные данные
        :param directed: Ориентированный?
        :return: Количество вершин
        """
        data = []
        rows = input_data.split('\n')
        for row in rows:
            if not row:
                pass
            elems = row.split(' ')
            if len(elems) < 2 or len(elems) > 3:
                raise ValueError('Некорректные входные данные')
            if len(elems) == 2:
                elems.append('')  # Если нет подписи - ставим пустую
            data.append(elems)
        nodes_count = draw(len(data), data, directed)
        return nodes_count

    def form_valid(self, form):
        input_data = form.cleaned_data['initial_data']
        is_directed = form.cleaned_data['directed']
        nodes_count = self.process_file(input_data.replace('\r', ''), is_directed)
        form.instance.graph_html = File(open(DEFAULT_PATH))
        form.instance.graph_html.name = DEFAULT_FILENAME
        form.instance.nodes_count = nodes_count

        result = super().form_valid(form)
        return result


class GraphDetailView(DetailView):
    model = Graph

    template_name = 'builder/detail.html'
