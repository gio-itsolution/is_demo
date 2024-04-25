from django.http import HttpResponseRedirect
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .forms import MyCallInfoForm


@main_auth(on_cookies=True)
def my_reg_call(request):
    but = request.bitrix_user_token
    if request.method == 'POST':
        form = MyCallInfoForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save(commit=False)
            model.file.save(model.file.name, model.file, save=False)
            model.lead_add = form.cleaned_data['add_entity']
            model.my_telephony_externalcall_register(but)
            model.my_telephony_externalcall_finish(but)
            model.save()
            if model.lead_id:
                lead_url = f'https://tte2.bitrix24.ru/crm/lead/details/{model.lead_id}/'
    form = MyCallInfoForm()
    return render(request, 'call_register.html', locals())
