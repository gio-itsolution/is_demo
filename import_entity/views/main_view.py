import os

import pandas as pd
import requests

from django.shortcuts import render

import settings
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.its_utils.app_get_params import get_params_from_sources
from callsuploader.models.models import CallInfo


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
        dfs['Компании']['COMPANY_IDS'] = ''
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
                    # Добавляем id созданных компаний в таблицу контактов и компаний
                    if entity_type == 4:
                        for res_item, row_entity in zip(res['items'], entity_data):
                            # Ищем пересечения между компаниями и контактами по ORIGIN_ID И вставляем туда значения id,
                            # полученных при импорте компаний
                            dfs['Контакты'].loc[dfs['Контакты']['COMPANY_ORIGIN_ID'] == row_entity['ORIGIN_ID'], 'COMPANY_IDS'] = int(res_item['item']['id'])
                            dfs['Компании'].loc[
                                dfs['Компании']['ORIGIN_ID'] == row_entity['ORIGIN_ID'], 'COMPANY_IDS'] = int(
                                res_item['item']['id'])

                    entity_data = []

            if len(entity_data) > 0:
                res = but.call_list_method('crm.item.batchImport', {'entityTypeId': entity_type,
                                                                    'data': entity_data})
                # Добавляем id созданных компаний в таблицу контактов  и компаний
                if entity_type == 4:
                    for res_item, row_entity in zip(res['items'], entity_data):
                        # Ищем пересечения между компаниями и контактами по ORIGIN_ID И вставляем туда значения id,
                        # полученных при импорте компаний
                        dfs['Контакты'].loc[
                            dfs['Контакты']['COMPANY_ORIGIN_ID'] == row_entity['ORIGIN_ID'], 'COMPANY_IDS'] = int(res_item['item']['id'])
                        dfs['Компании'].loc[
                            dfs['Компании']['ORIGIN_ID'] == row_entity['ORIGIN_ID'], 'COMPANY_IDS'] = int(
                            res_item['item']['id'])
            # Добавляем адреса
            if entity_type == 4:
                for index, row in df.iterrows():
                    but.call_api_method("crm.address.add", {"fields": {
                        "TYPE_ID": "1",  # Фактический адрес
                        "ENTITY_TYPE_ID": entity_type,  # 4 - для Компаний
                        "ENTITY_ID": row.COMPANY_IDS,
                        "CITY": row.ADDRESS_CITY,
                        "ADDRESS_1": row.ADDRESS,
                    }})

            entity_type -= 1

        # Добавляем звонки
        calls_df = pd.read_excel(export_link, sheet_name='Звонки')
        for index, row in calls_df.iterrows():
            call = CallInfo(
                user_phone=row.user_phone,
                user_id=int(row.user_id),
                phone_number=row.phone_number,
                call_date=row.call_date,
                type=row.type,
                add_to_chat=row.add_to_chat
            )
            call.save()

            drive_id = row.file.split("/")[-2]
            url = "https://drive.google.com/uc?id=" + drive_id + "&export=download"
            r = requests.get(url, allow_redirects=True)
            file_path = os.path.join(call.inner_media_path, str(call.id) + '.mp3')
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            with open(full_path, 'wb') as file:
                file.write(r.content)
            call.file.name = file_path
            call.save()

            call.telephony_externalcall_register(but)
            call.telephony_externalcall_finish(but)
            os.remove(full_path)

    return render(request, 'main_page_entity.html')
