def find_supervisor(departments_dict: dict, current_dep: str = '1', order: int = 0) -> tuple:
    """
    Рурсивая функция, осуществляющая поиск начальника для пользователя, если в настоящем
    подразделении он не был найден.ек
    """

    department = departments_dict[current_dep]
    parent_exists = ('PARENT' in department)
    supervisor = department.get('UF_HEAD')
    supervisor_exists = (supervisor and (supervisor != '0'))

    if supervisor_exists:
        return department['UF_HEAD'], order
    else:
        if not parent_exists:
            return "None", order
        return find_supervisor(departments_dict, department['PARENT'], order + 1)

def my_search_manager(but) -> tuple:
    """
    Принимает пользователя и осуществляет поиск начальников для него.
    Возвращает кортеж из словаря с начальниками и списка с полями
    """

    users = but.call_list_method('user.get')
    departments = but.call_list_method('department.get')

    user_fields = ['NAME', 'LAST_NAME', 'SECOND_NAME', 'UF_DEPARTMENT']
    user_dict = {}
    departments_dict = {}

    def fill_user_and_dep_dicts():
        """
        Функция заполняет словари user_dict и departments_dict.
        Ключом выступает Id, значением словарь типа {'Название поля': 'Значение поля'}
        """
        for dep_elem in departments:
            departments_dict.update({dep_elem['ID']: dep_elem})
            departments_dict[dep_elem['ID']].pop('ID')

        for elem in users:
            user_dict.update({elem['ID']: {}})
            for field in user_fields:
                if field == 'UF_DEPARTMENT':
                    user_dict[elem['ID']][field] = {}
                    for dep_id in elem[field]:
                        user_dict[elem['ID']][field].update({dep_id: departments_dict[str(dep_id)]['NAME']})
                else:
                    try:
                        user_dict[elem['ID']].update({field: elem[field]})
                    except KeyError:
                        pass

    def find_head_for_users():
        """
        Функция проходится по пользователям и ищет для каждого руководителей
        во всех подразделениях
        """
        # Проходимся по всем юзерам, для каждого ищем руководителей
        for user_id in user_dict:
            user = user_dict[user_id]

            # Руководителей записываем в list
            user.update({'SUPERVISORS': list()})
            for department_id in user['UF_DEPARTMENT']:
                department_id = str(department_id)
                # Смотрим, состоит ли человек в текущем подразделении.
                # Если состоит, то в качестве кого?
                if departments_dict[department_id].get('UF_HEAD') == user_id:
                    if 'PARENT' in departments_dict[department_id]:
                        department = departments_dict[department_id]['PARENT']
                        supervisor_id, order = find_supervisor(departments_dict, department)
                    else:
                        supervisor_id = 'None'
                else:
                    if int(department_id) in user['UF_DEPARTMENT']:
                        department = department_id
                        supervisor_id, order = find_supervisor(departments_dict, department)
                    else:
                        continue

                if supervisor_id != 'None':
                    supervisor = user_dict[supervisor_id]
                    conj_str = ""
                    for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
                        try:
                            conj_str += f'{supervisor[key]}'
                        except KeyError:
                            pass
                    conj_str += f'| ID: {supervisor_id} | Порядок: {order}'
                    user['SUPERVISORS'].append((supervisor_id, conj_str))
            if user['SUPERVISORS'] == list():
                user['SUPERVISORS'] = ''

    fill_user_and_dep_dicts()
    find_head_for_users()

    return user_dict, user_fields
