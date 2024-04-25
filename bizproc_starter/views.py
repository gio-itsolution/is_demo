from django.shortcuts import render

from .forms import MyBPForm
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from .models import MyBizprocModel


@main_auth(on_cookies=True)
def run_bizproc(request):
    but = request.bitrix_user_token


    if request.method == 'POST':
        entity = request.POST.get('entity')
        form = MyBPForm(request.POST)
        if form.is_valid():
            entity_ids = but.call_list_method(f'crm.{entity.lower()}.list', {'select': ['ID']})
            cur_bp = form.cleaned_data['bp']
            for elem in entity_ids:
                cur_bp.run_cur_bizproc(but, elem['ID'], entity)
    else:
        entity = request.GET.get('entity')
        MyBizprocModel.find_all_bizprocs(but, entity)
        form = MyBPForm()
        form.fields['bp'].queryset = MyBizprocModel.objects.filter(process_entity=entity)

    return render(request, 'bizprocstarter.html', context={'form': form, 'entity': entity})


@main_auth(on_cookies=True)
def main_page(request):
    '''
    Render app main page
    '''
    return render(request, 'main_page_bizproc.html')
