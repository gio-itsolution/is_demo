from django.urls import path

from .views import find_duplicates, main_page

app_name = 'my_duplicate_searcher'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('finded_duplicates/', find_duplicates, name='duplicate_finder'),
]
