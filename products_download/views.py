from django.http import HttpResponse
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from .utils import excel_table_create


@main_auth(on_cookies=True)
def main_page(request):
    '''
    Генерирует страницу с таблицей, содержащюю первые 5 товарных позиций, с возможностью загрузки товаров в xlsx
    '''
    if request.method == 'POST':
        with open('media/files/Products.xlsx', 'rb') as f:
            file_content = f.read()

            response = HttpResponse(file_content, content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=products.xlsx'
            response['Refresh'] = 'download_products.html'
        return response

    but = request.bitrix_user_token
    products = but.call_list_method('crm.product.list', {'SELECT': [
                                    'ID', 'NAME',
                                    'PRICE', 'DESCRIPTION',
                                    'CATALOG_ID', 'SECTION_ID']})

    products = {product['ID']: product for product in products}
    products_df = excel_table_create(products)

    return render(request, 'download_products.html', {'df': products_df})
