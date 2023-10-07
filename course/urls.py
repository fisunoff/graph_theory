from django.urls import path

from course.views.course_views import CourseListView, CourseCreateView, CourseDetailView, CourseUpdateView
from course.views.lesson_views import LessonCreateView, LessonDetailView, LessonUpdateView

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('create/', CourseCreateView.as_view(), name='course-create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('lesson/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('lesson/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
]
