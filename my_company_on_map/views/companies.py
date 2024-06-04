from django.http import JsonResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def companies(request):
    """Возвращает JSON со списком компаний с известными адресами"""
    but = request.bitrix_user_token
    # all_companies = but.call_list_method("crm.company.list", {
    #     "select": ["ID", "TITLE"]
    # })
    all_contacts = but.call_list_method("crm.contact.list", {"select": ["ID", "NAME", "PHOTO"]})
    all_contacts = {c["ID"]: c for c in all_contacts}

    if len(all_contacts) == 0:
        return JsonResponse({})

    all_addresses = but.call_list_method("crm.address.list", {
        "order": {"TYPE_ID": "ASC"},
        "select": ["ADDRESS_1", "CITY", "PROVINCE", "COUNTRY", "ANCHOR_ID"],
        "filter": {
            "ANCHOR_TYPE_ID": "3"
        }
    })

    if len(all_addresses) == 0:
        return JsonResponse({})

    conts_w_addr = {}
    for a in all_addresses:
        cont_id = a["ANCHOR_ID"]
        if not all_contacts.get(cont_id):
            continue

        cont = conts_w_addr.setdefault(cont_id, {})
        cont.setdefault("addr", []).append(a)
        cont["name"] = all_contacts[cont_id]["NAME"]
        cont["cont_id"] = cont_id
        if all_contacts[cont_id]["PHOTO"] is not None:
            cont["photo"] = all_contacts[cont_id]["PHOTO"]['downloadUrl']

    return JsonResponse(conts_w_addr)
