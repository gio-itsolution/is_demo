from django.conf import settings

from integration_utils.bitrix24.bitrix_token import BitrixToken


def get_token() -> BitrixToken:
    """Получение токена по авторизации из хука с нужными скоупами."""

    return BitrixToken(web_hook_auth=settings.HOOK_TOKEN, domain=settings.APP_SETTINGS.portal_domain)
