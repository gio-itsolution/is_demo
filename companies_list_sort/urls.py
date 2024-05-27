from django.urls import path

from companies_list_sort.views.views import sort_companies_list

app_name = 'companies_list_sort'

urlpatterns = [
    path('', sort_companies_list,
         name='sort_list'),
]
