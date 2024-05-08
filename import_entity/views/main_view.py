import pandas as pd

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.its_utils.app_get_params import get_params_from_sources


@get_params_from_sources
@main_auth(on_cookies=True)
def main_page(request):
    '''
    Функция получает на вход xlsx/csv файл с сущностями и импортирует их
    '''
    if request.method == 'POST':
        but = request.bitrix_user_token

        link = request.its_params['excel_url']
        export_link = "/".join(link.split("/")[0:-1]) + "/export"

        dfs = pd.read_excel(export_link, sheet_name=['Компании', 'Контакты', 'Сделки', 'Лиды'])

        entity_type = 4

        dfs['Контакты']['COMPANY_IDS'] = ''
        for entity_name, df in dfs.items():
            counter = 0
            entity_data = []
            for index, row in df.iterrows():
                data_dict = {}
                for column, value in row.items():
                    data_dict[column] = value
                entity_data.append(data_dict)
                counter += 1
                if counter % 20 == 0:
                    res = but.call_list_method('crm.item.batchImport', {'entityTypeId': entity_type,
                                                                        'data': entity_data})
                    # Добавляем id созданных компаний в таблицу контактов
                    if entity_type == 4:
                        for res_item, row_entity in zip(res['items'], entity_data):
                            # Ищем пересечения между компаниями и контактами по ORIGIN_ID И вставляем туда значения id,
                            # полученных при импорте компаний
                            dfs['Контакты'].loc[dfs['Контакты']['COMPANY_ORIGIN_ID'] == row_entity['ORIGIN_ID'], 'COMPANY_IDS'] = int(res_item['item']['id'])

                    entity_data = []

            if len(entity_data) > 0:
                res = but.call_list_method('crm.item.batchImport', {'entityTypeId': entity_type,
                                                                    'data': entity_data})
                # Добавляем id созданных компаний в таблицу контактов
                if entity_type == 4:
                    for res_item, row_entity in zip(res['items'], entity_data):
                        # Ищем пересечения между компаниями и контактами по ORIGIN_ID И вставляем туда значения id,
                        # полученных при импорте компаний
                        dfs['Контакты'].loc[
                            dfs['Контакты']['COMPANY_ORIGIN_ID'] == row_entity['ORIGIN_ID'], 'COMPANY_IDS'] = int(res_item['item']['id'])
            entity_type -= 1

    return render(request, 'main_page_entity.html')
