from django.urls import path
from . import views

urlpatterns = [
    path('sorting/bubble/', views.bubble_sort_view, name='bubble_sort'),
]