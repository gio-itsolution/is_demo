from django.urls import path

from .views.handler import index, handler
from .views.install import main_page, install, uninstall

app_name = 'show_user_info'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('install/', install, name='install'),
    path('uninstall/', uninstall, name='uninstall'),
    path('frame_main', index, name='frame_main'),
    path('handler_main/', handler, name='get_user_info'),

]
