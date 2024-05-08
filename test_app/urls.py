from django.urls import path

from .views import main_page

app_name = 'test_app'

urlpatterns = [
    path('', main_page, name='main_page'),
]
