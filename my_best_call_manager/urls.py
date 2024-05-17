from django.urls import path

from my_best_call_manager.views.find_finish_task import my_find_finish_task
from my_best_call_manager.views.start_function import my_start_find_all_call

app_name = 'my_best_call_manager'

urlpatterns = [
    path('start_find_all_call/', my_start_find_all_call,
         name='my_start_find_all_call'),
    path('finish_find_all_call/', my_find_finish_task,
         name='my_find_finish_task'),
]
