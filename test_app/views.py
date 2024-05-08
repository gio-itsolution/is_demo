from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


def main_page(request):
    '''
    Render app main page
    '''
    return render(request, 'main_test_page.html')
