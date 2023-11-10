from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from course.models import Lesson, Step
from course.tables import StepTable
from course.views.mixins import AddTitleFormMixin, DetailWithSingleTable, SaveEditorMixin
from funcs import OnlyCreatorMixin, OnlyParentCreatorMixin


class LessonCreateView(OnlyParentCreatorMixin, LoginRequiredMixin, SaveEditorMixin, AddTitleFormMixin, CreateView):
    model = Lesson
    template_name = 'base_create.html'

    fields = ('name', 'description', 'course')

    title = "Добавление урока"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
        initial_data['course'] = self.kwargs['from']
        return initial_data

    def get_success_url(self):
        return reverse_lazy('lesson-detail', kwargs={'pk': self.object.id})


class LessonDetailView(DetailWithSingleTable):
    model = Lesson
    template_name = 'lesson/detail.html'

    table_model = Step
    table_class = StepTable

    def get_table_data(self):
        lesson = self.object.id
        return self.table_model.objects.filter(lesson=lesson)


class LessonUpdateView(OnlyCreatorMixin, LoginRequiredMixin, AddTitleFormMixin, UpdateView):
    model = Lesson
    template_name = 'base_create.html'

    title = 'Редактирование урока'
    editing = True

    fields = ('name', 'description')
