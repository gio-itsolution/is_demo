from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from film_find_robot.models.robot_film_find_model import FilmRobot


@main_auth(on_cookies=True)
def robot_currency(request):

    return render(request, 'robot_currency_temp.html', locals())
