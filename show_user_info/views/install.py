from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from integration_utils.bitrix24.models import BitrixUser

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def main_page(request):
    return render(request, 'install_window.html')


@main_auth(on_cookies=True)
def install(request):
    """
    Функция производит встраивание в карточку сделки
    """
    if request.method == 'POST':
        handler = 'https://' + settings.DOMAIN + reverse('show_user_info:frame_main')
        but = request.bitrix_user_token
        try:
            but.call_api_method('placement.bind', {'PLACEMENT': 'CRM_DEAL_DETAIL_TAB', 'HANDLER': handler})
            messages.success(request, 'Окно успешно добавлено!')
        except Exception as e:
            messages.error(request, f'Ошибка: {e}')

    return render(request, 'install_window.html')

@main_auth(on_cookies=True)
def uninstall(request):
    """
    Функция производит удаление из карточки сделки
    """
    but = request.bitrix_user_token
    if request.method == 'POST':
        handler = 'https://' + settings.DOMAIN + reverse('show_user_info:frame_main')
        but = request.bitrix_user_token
        try:
            but.call_api_method('placement.unbind', {'PLACEMENT': 'CRM_DEAL_DETAIL_TAB', 'HANDLER': handler})
            messages.success(request, 'Окно успешно удалено!')
        except Exception as e:
            messages.error(request, f'Ошибка: {e}')

    return render(request, 'install_window.html')
