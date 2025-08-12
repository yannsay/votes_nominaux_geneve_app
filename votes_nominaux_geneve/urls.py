from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('selection-rsge', views.selection_rsge, name = 'selection-rsge'),
    path('table-votes', views.plot_votes_table, name = 'table-votes'),
    path('about', views.about, name = 'about'),
]