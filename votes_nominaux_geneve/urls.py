from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('selection-rgse', views.selection_rgse, name = 'selection-rgse')
]