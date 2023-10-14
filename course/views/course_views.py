from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django_tables2 import SingleTableView
from course.models import Course, Lesson
from course.tables import CourseTable, LessonTable
from course.views.mixins import AddTitleFormMixin, DetailWithSingleTable
# Create your views here.


class CourseListView(SingleTableView):
    model = Course
    template_name = 'base_list.html'
    table_class = CourseTable

    def get_queryset(self):
        return Course.objects.all()


class CourseCreateView(AddTitleFormMixin, CreateView):
    model = Course
    template_name = 'course/create.html'
    success_url = reverse_lazy('course-list')

    fields = ('name', 'description', 'private', 'password')

    title = "Создание курса"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
        return initial_data


class CourseDetailView(DetailWithSingleTable):
    model = Course
    table_model = Lesson

    table_class = LessonTable
    template_name = 'course/detail.html'

    def get_table_data(self):
        course_id = self.object.id
        return self.table_model.objects.filter(course=course_id)


class CourseUpdateView(AddTitleFormMixin, UpdateView):
    model = Course
    template_name = 'course/create.html'

    title = 'Редактирование курса'
    editing = True

    fields = ('name', 'description', 'private', 'password')
