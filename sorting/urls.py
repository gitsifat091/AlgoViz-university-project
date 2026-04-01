from django.urls import path
from . import views

urlpatterns = [
    path('sorting/bubble/',    views.bubble_sort_view,    name='bubble_sort'),
    path('sorting/selection/', views.selection_sort_view, name='selection_sort'),
    path('sorting/insertion/', views.insertion_sort_view, name='insertion_sort'),
    path('sorting/merge/',     views.merge_sort_view,     name='merge_sort'),
    path('sorting/quick/',     views.quick_sort_view,     name='quick_sort'),
]