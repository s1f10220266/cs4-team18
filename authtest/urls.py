from django.urls import path
from . import views
from .views import todo_list

urlpatterns = [
    path('', views.home, name='home'),
    path('/todoWithoutLogin', views.withoutLogin, name="withoutLogin"),
    path('todo/', views.todo_list, name='todo_list'),
    path('detail/<int:todo_id>/', views.detail, name="detail"),
    path('edit/<int:todo_id>/', views.edit, name="edit"),
]