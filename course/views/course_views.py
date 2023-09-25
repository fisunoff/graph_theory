from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_tables2 import SingleTableView
from course.models import Course
from course.tables import CourseTable
from course.views.mixins import AddTitleFormMixin
from funcs import group_required
# Create your views here.


class CourseListView(SingleTableView):
    model = Course
    template_name = 'course/list.html'
    table_class = CourseTable

    def get_queryset(self):
        return Course.objects.all()


class CourseCreateView(AddTitleFormMixin, CreateView):
    model = Course
    template_name = 'course/create.html'
    success_url = reverse_lazy('courses-list')

    fields = ('name', 'description', 'private', 'password')

    title = "Создание курса"

    def get_initial(self):
        initial_data = {}
        for i in self.fields:
            initial_data[i] = self.request.GET.get(i)
        return initial_data
