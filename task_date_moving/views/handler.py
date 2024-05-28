from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib import messages

from integration_utils.bitrix24.models import BitrixUser
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

@main_auth(on_start=True, set_cookie=True)
def task_moving(request):
    return render(request, 'button_move.html')

@main_auth(on_cookies=True)
def task_handler(request):
    if request.method == 'POST':
        user_but = request.bitrix_user_token
        admin_but = BitrixUser.objects.filter(is_admin=True,
                                        user_is_active=True).first().bitrix_user_token

        task_id = request.POST['task_id']
        deadline = admin_but.call_api_method('tasks.task.get', {'taskId': task_id})['result']['task']['deadline']
        created_by = admin_but.call_api_method('tasks.task.get', {'taskId': task_id})['result']['task']['createdBy']
        if int(created_by) == user_but.user_id:
            datetime_obj = datetime.fromisoformat(deadline)
            new_datetime_obj = datetime_obj + timedelta(days=1)
            new_deadline = new_datetime_obj.isoformat()

            admin_but.call_api_method('tasks.task.update', {'taskId': task_id, 'fields': {'DEADLINE': new_deadline}})
            messages.success(request, 'Дата успешно подвинута!')
        else:
            messages.error(request, 'Пользователь не является постановщиком!')

    return render(request, 'button_move.html')


