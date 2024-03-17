from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('calculate/', CalcView.as_view(), name='calculate'),
    path(r'', TemplateView.as_view(template_name='sets/main.html'), name='sets-main'),
]
