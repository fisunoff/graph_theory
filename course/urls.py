from django.urls import path

from course.views.course_views import CourseListView, CourseCreateView

urlpatterns = [
    path('', CourseListView.as_view(), name='courses-list'),
    path('create/', CourseCreateView.as_view(), name='courses-create'),

]
