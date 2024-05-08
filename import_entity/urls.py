from django.urls import path
from .views.main_view import main_page

app_name = 'import_entity'

urlpatterns = [
    path('', main_page, name='main_page'),
]
