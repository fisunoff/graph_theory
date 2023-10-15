from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from course.models import Step
from course.views.mixins import AddTitleFormMixin, DetailWithSingleTable, ProDetailView, SaveEditorMixin


class StepCreateView(SaveEditorMixin, AddTitleFormMixin, CreateView):
    model = Step
    template_name = 'step/create.html'
    success_url = reverse_lazy('course-list')

    fields = ('name', 'lesson', 'data')
    title = "Добавление шага"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
            initial_data['lesson'] = self.kwargs['from']
        return initial_data


class StepDetailView(ProDetailView):
    model = Step
    template_name = 'step/detail.html'


# class LessonUpdateView(AddTitleFormMixin, UpdateView):
#     model = Lesson
#     template_name = 'base_create.html'
#
#     title = 'Редактирование урока'
#     editing = True
#
#     fields = ('name', 'description')
