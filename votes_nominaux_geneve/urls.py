from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('selection-rsge', views.selection_rsge, name = 'selection-rsge'),
    path('table-votes', views.create_votes_table, name = 'table-votes'),
    path('about', views.about, name = 'about'),
    path('download_votes_csv/', views.download_votes_csv, name='download_votes_csv')
]