from django.urls import path

from .views import main_page

app_name = 'products_download'

urlpatterns = [
    path('main/', main_page, name='main_page'),
]
