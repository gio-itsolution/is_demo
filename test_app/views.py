from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


def main_page(request):
    '''
    Render app main page
    '''
    test_var1 = (1, 2, 3)
    test_var2 = (1, 2, 3,)
    return render(request, 'test_page_2.html')
