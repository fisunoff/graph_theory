from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from course.models import Task
from course.views.mixins import AddTitleFormMixin, DetailWithSingleTable, ProDetailView, SaveEditorMixin


class TaskCreateView(LoginRequiredMixin, SaveEditorMixin, AddTitleFormMixin, CreateView):
    model = Task
    template_name = 'task/create.html'

    fields = ('name', 'step', 'description', 'graph', 'max_mark', 'weight', 'auto_test', 'correct_answers')
    title = "Добавление задания"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
            initial_data['step'] = self.kwargs['from']
        return initial_data

    def get_success_url(self):
        return reverse_lazy('step-detail', kwargs={'pk': self.object.step.id})


class TaskDetailView(ProDetailView):
    model = Task
    template_name = 'task/detail.html'

