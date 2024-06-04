from django.urls import path

from .views.my_company_on_map import company_on_map
from .views.companies import companies

app_name = 'show_company_on_map'

urlpatterns = [
    path('', company_on_map, name='main_page'),
    path('handler/', companies, name='handler'),
]
