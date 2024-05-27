import locale

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from companies_list_sort.funcs.get_token import get_token
from companies_list_sort.forms import FieldSelectionForm

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


# Create your views here.


@main_auth(on_cookies=True)
def sort_companies_list(request):
    but = request.bitrix_user_token
    # but = get_token()

    if request.method == "POST":
        form = FieldSelectionForm(request.POST)
        # res = but.call_list_method('crm.company.userfield.list', {'FILTER': {'FIELD_NAME': 'UF_CRM_1715953735'}})[0]
        #
        # field_id = res['ID']
        # comp_list = res['LIST']
        #
        # def sort_companies_by_name(company_list):
        #     locale.setlocale(locale.LC_ALL, '')
        #
        #     def sort_key(item):
        #         return locale.strxfrm(item['VALUE'])
        #
        #     sorted_companies = sorted(company_list, key=sort_key)
        #     for index, company in enumerate(sorted_companies):
        #         company['SORT'] = index
        #     return sorted_companies
        #
        # sorted_data = sort_companies_by_name(comp_list)
        #
        # but.call_list_method('crm.company.userfield.update', {'ID': field_id, 'FIELDS': {'LIST': sorted_data}})


    else:
        form = FieldSelectionForm(request.POST)
        form.find_user_fields(but)

    return render(request, 'main.html', {'form': form})

