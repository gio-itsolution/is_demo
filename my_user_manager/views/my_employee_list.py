from django.shortcuts import render
from ..utils.my_search_manager import my_search_manager
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def my_employee_list(request):
    but = request.bitrix_user_token
    user_dict, user_fields = my_search_manager(but)

    return render(request, 'my_list.html', context={'fields': user_fields, 'users': user_dict})
