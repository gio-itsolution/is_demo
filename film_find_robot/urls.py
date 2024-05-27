from django.urls import path

from .models.robot_film_find_model import FilmRobot
from .views.install import install
from .views.robot_currency_view import robot_currency
from .views.uninstall import uninstall

app_name = 'bitrix_film_robot'

urlpatterns = [
    path('home/', robot_currency, name='robot_film_home'),
    path('install/', install, name='install_robot'),
    path('uninstall/', uninstall, name='uninstall_robot'),
    path('handler/', FilmRobot.as_view(), name='handler_robot'),
]
