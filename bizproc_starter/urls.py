from django.urls import path

from .views import run_bizproc, main_page

app_name = 'bizproc_starter'

urlpatterns = [
    path('starter/', run_bizproc, name='starter'),
    path('main/', main_page, name='main_page'),
]
