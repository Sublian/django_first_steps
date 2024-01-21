from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('other/', views.other, name='other'),
    path('hello/<str:username>', views.hello, name='hello'),
    path('proyects/<int:id>', views.proyect_detail, name='proyects_detail'),
    path('proyects/', views.proyects, name='proyects'),
    path('create_proyects/', views.create_proyect, name='create_proyect'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('create_tasks/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', views.signout, name='signout'),
    path('signin/', views.signin, name='signin'),
    
]