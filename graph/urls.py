# from django.urls import path
# from . import views

# urlpatterns = [
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('graph/bfs/',          views.bfs_view,          name='bfs'),
    path('graph/dfs/',          views.dfs_view,          name='dfs'),
    path('graph/dijkstra/',     views.dijkstra_view,     name='dijkstra'),
    path('graph/bellman-ford/', views.bellman_ford_view, name='bellman_ford'),
]