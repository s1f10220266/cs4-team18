from django.urls import path
from . import views
from .views import todo_list

urlpatterns = [
    path('', views.home, name='home'),
    path('todo', views.todo_list, name='todo_list'),
]