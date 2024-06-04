import json

from django.http import JsonResponse
from django.shortcuts import render


from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def main_page(request):

    but = request.bitrix_user_token
    res = but.call_api_method("user.get", {})['result']
    json_user_list = json.dumps(res)

    return render(request, 'main_page_AG.html', context={'user_list': json_user_list})

