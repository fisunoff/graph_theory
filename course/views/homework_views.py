from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from course.models import HomeWork, Task
from course.views.mixins import AddTitleFormMixin, DetailWithSingleTable, ProDetailView, SaveEditorMixin
from extended_user.models import Profile


class HomeworkCreateView(LoginRequiredMixin, SaveEditorMixin, AddTitleFormMixin, CreateView):
    model = HomeWork
    template_name = 'base_create.html'

    fields = ('description', )
    title = "Добавление решения"

    save_creator_only = True

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
        return initial_data

    def get_success_url(self):
        return reverse_lazy('homework-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        task_pk = self.kwargs['from']
        task = Task.objects.get(pk=task_pk)
        if task.auto_test:
            student_answer = form.cleaned_data['description']
            if student_answer.lower().strip() in task.correct_answers.split(';'):
                form.instance.mark = task.max_mark
            else:
                form.instance.mark = 0
        form.instance.task = task
        result = super().form_valid(form)
        return result


class HomeworkDetailView(ProDetailView):
    model = HomeWork
    template_name = 'homework/detail.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        can_edit = False
        if self.request.user.is_authenticated:
            can_edit = self.request.user.profile.pk == self.object.is_parent_creator or self.request.user.is_superuser
        kwargs['can_edit'] = can_edit
        return kwargs


class HomeworkUpdateView(SaveEditorMixin, LoginRequiredMixin, AddTitleFormMixin, UpdateView):
    model = HomeWork
    template_name = 'base_create.html'

    title = 'Оценка решения'
    editing = True

    fields = ('description', 'mark')

    def form_valid(self, form):
        self.object = form.save()
        user_profile = Profile.objects.get(id=self.request.user.profile.id)
        if not self.save_creator_only:
            self.object.last_editor = user_profile
        if not self.object.creator:
            self.object.creator = user_profile
        if self.object.mark > self.object.task.max_mark:
            form.add_error('mark', f'Оценка больше максимально возможной {self.object.mark}/{self.object.task.max_mark}')
            return self.form_invalid(form)
        elif self.object.mark < 0:
            form.add_error('mark', 'Оценка не может быть меньше 0')
            return self.form_invalid(form)

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
