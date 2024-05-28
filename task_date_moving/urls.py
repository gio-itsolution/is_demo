from django.urls import path

from .views.handler import task_moving, task_handler

app_name = 'task_date_moving'

urlpatterns = [
    path('handler/', task_moving, name='handler_task'),
    path('handler_main/', task_handler, name='handler_task_main'),
]
