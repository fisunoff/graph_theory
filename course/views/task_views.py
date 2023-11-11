from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from course.models import Task, HomeWork
from course.tables import HomeWorkTable
from course.views.mixins import AddTitleFormMixin, DetailWithSingleTable, ProDetailView, SaveEditorMixin
from funcs import OnlyParentCreatorMixin


class TaskCreateView(OnlyParentCreatorMixin, LoginRequiredMixin, SaveEditorMixin, AddTitleFormMixin, CreateView):
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


class TaskDetailView(DetailWithSingleTable):
    model = Task
    template_name = 'task/detail.html'

    table_model = HomeWork
    table_class = HomeWorkTable

    def get_table_data(self):
        task = self.object.id
        task_obj = Task.objects.get(pk=task)
        if not self.request.user.is_authenticated:
            return self.table_model.objects.none()
        if self.request.user.profile == task_obj.creator or self.request.user.is_superuser:
            return self.table_model.objects.filter(task_id=task)
        else:
            return self.table_model.objects.filter(task_id=task, creator=self.request.user.profile)

    def get_table_kwargs(self):
        kwargs = {}
        if self.request.user.is_authenticated:
            if self.request.user.profile in (self.object.creator, self.object.last_editor) \
                    or self.request.user.is_superuser:
                kwargs['exclude'] = ('title', )
            else:
                kwargs['exclude'] = ('title_with_author', )
        return kwargs
