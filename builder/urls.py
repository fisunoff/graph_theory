from django.urls import path

from builder.views import GraphDetailView, GraphCreateView, GraphListView

urlpatterns = [
    path('', GraphListView.as_view(), name='graph-list'),
    path('create/', GraphCreateView.as_view(), name='graph-create'),
    path('<int:pk>/', GraphDetailView.as_view(), name='graph-detail'),
]
