from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from collections import Counter


@main_auth(on_cookies=True)
def find_duplicates(request):
    '''
    Find docs duplicates
    '''
    method_list = {
        'company': 'компаний',
        'lead': 'лидов',
        'deal': 'сделок',
        'contact': 'контактов',
        'product': 'товаров'
    }
    lst = list()

    but = request.bitrix_user_token
    form = request.GET
    method = form.get('method')
    res = but.call_list_method(f'crm.{method}.list')

    match method:
        case 'product' | 'contact':
            for i in res:
                lst.append(i["NAME"])
        case 'deal' | 'lead' | 'company':
            for i in res:
                lst.append(i["TITLE"])
    method_word = method_list[method]
    res = {name: count for name, count in Counter(lst).items() if count > 1}

    return render(request, 'my_duplicate.html', context={'res': res, 'method_word': method_word})

@main_auth(on_cookies=True)
def main_page(request):
    '''
    Render app main page
    '''
    return render(request, 'main_page.html')