# from django.urls import path
# from . import views

# urlpatterns = [
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('graph/bfs/',            views.bfs_view,            name='bfs'),
    path('graph/dfs/',            views.dfs_view,            name='dfs'),
    path('graph/dijkstra/',       views.dijkstra_view,       name='dijkstra'),
    path('graph/bellman-ford/',   views.bellman_ford_view,   name='bellman_ford'),
    path('graph/floyd-warshall/', views.floyd_warshall_view, name='floyd_warshall'),
    path('graph/best-first/',     views.best_first_view,     name='best_first'),
    path('graph/ucs/',            views.ucs_view,            name='ucs'),
    path('graph/dls/',            views.dls_view,            name='dls'),
]