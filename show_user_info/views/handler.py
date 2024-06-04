from django.http import JsonResponse
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

@main_auth(on_start=True, set_cookie=True)
def index(request):
    return render(request, 'main_show.html')


@main_auth(on_cookies=True)
def handler(request):
    if request.method == 'POST':
        but = request.bitrix_user_token
        user_id = request.POST['id']
        res = but.call_api_method("user.get", {'ID': user_id})['result'][0]

        return JsonResponse({'status': 'ok', 'res': res})
    return JsonResponse({'status': 'error'})
