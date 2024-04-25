from django.urls import path

from .views import my_reg_call

app_name = 'my_calls'

urlpatterns = [
    path('my_register_call/', my_reg_call, name='my_register_call'),
]
