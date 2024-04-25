from django.urls import path

from .views.my_employee_list import my_employee_list

app_name = 'my_employee_list'

urlpatterns = [
    path('', my_employee_list, name='main_page'),
]
