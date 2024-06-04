from django.urls import path

from .views.main_view import main_page

app_name = 'show_user_info_AG'

urlpatterns = [
    path('', main_page, name='main_page'),
]
