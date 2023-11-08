from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from course.models import Step, Task
from course.tables import TaskTable
from course.views.mixins import AddTitleFormMixin, DetailWithSingleTable, ProDetailView, SaveEditorMixin


class StepCreateView(LoginRequiredMixin, SaveEditorMixin, AddTitleFormMixin, CreateView):
    model = Step
    template_name = 'step/create.html'

    fields = ('name', 'lesson', 'data', 'graph')
    title = "Добавление шага"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
            initial_data['lesson'] = self.kwargs['from']
        return initial_data

    def get_success_url(self):
        return reverse_lazy('lesson-detail', kwargs={'pk': self.object.lesson.id})


class StepDetailView(DetailWithSingleTable):
    model = Step
    template_name = 'step/detail.html'

    table_model = Task
    table_class = TaskTable

    def get_table_data(self):
        step = self.object.id
        return self.table_model.objects.filter(step=step)

    def get_table_kwargs(self):
        kwargs = {'exclude': ('answer_count', )}
        if self.request.user in (self.object.creator, self.object.last_editor) \
            or self.request.user.is_superuser:
            kwargs['exclude'] = ()
        return kwargs
