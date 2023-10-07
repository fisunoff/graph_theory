from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from course.models import Lesson
from course.views.mixins import AddTitleFormMixin, ProDetailView
# Create your views here.


class LessonCreateView(AddTitleFormMixin, CreateView):
    model = Lesson
    template_name = 'base_create.html'
    success_url = reverse_lazy('courses-list')

    fields = ('name', 'description', 'course')

    title = "Добавление урока"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
        return initial_data


class LessonDetailView(ProDetailView):
    model = Lesson
    template_name = 'lesson/detail.html'


class LessonUpdateView(AddTitleFormMixin, UpdateView):
    model = Lesson
    template_name = 'base_create.html'

    title = 'Редактирование урока'
    editing = True

    fields = ('name', 'description')
