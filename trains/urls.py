from django.urls import path
from .views import TrainCreateView, TrainSearchView

urlpatterns = [
    path('create/', TrainCreateView.as_view(), name='train_create'),
    path('search/', TrainSearchView.as_view(), name='train_search'),
]