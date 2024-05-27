from django.http import HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from film_find_robot.models.robot_film_find_model import FilmRobot


@main_auth(on_cookies=True)
def uninstall(request):
    try:
        FilmRobot.uninstall(request.bitrix_user_token)
    except Exception as exc:
        return HttpResponse(str(exc))

    return HttpResponse('ok')
