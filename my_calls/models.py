import os

from django.conf import settings
from django.db import models
from mutagen.mp3 import MP3

class NumberChoicesType(models.IntegerChoices):
    one = 1, 'Исходящий'
    two = 2, 'Входящий'
    three = 3, 'Входящий с перенаправлением'
    four = 4, 'Обратный'


class NumberChoicesAddToChat(models.IntegerChoices):
    zero = 0, 'Не уведомлять'
    one = 1, 'Уведомлять'


class MyCallInfo(models.Model):
    user_phone = models.CharField(max_length=20, null=False, blank=False)
    user_id = models.IntegerField(blank=False, null=False)
    phone_number = models.CharField(max_length=50, null=False, blank=False)
    call_date = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(null=False, blank=False,
                               choices=NumberChoicesType.choices)
    duration = models.IntegerField(null=True, blank=True)
    add_to_chat = models.IntegerField(blank=True, null=True,
                                      choices=NumberChoicesAddToChat.choices)
    call_id = models.CharField(max_length=255, null=True, blank=True)
    lead_id = models.IntegerField(default=None, null=True, blank=True)

    inner_media_path = "rings/"
    filename = ""
    file = models.FileField(upload_to=inner_media_path, null=True, blank=True)

    def my_telephony_externalcall_register(self, but):

        register_params = {
            "USER_PHONE_INNER": self.user_phone,
            "USER_ID": self.user_id,
            "PHONE_NUMBER": self.phone_number,
            "CALL_START_DATE": self.call_date,
            "TYPE": self.type
        }
        if self.lead_add:
            register_params["CRM_CREATE"] = 1
        res = but.call_api_method("telephony.externalcall.register", register_params)

        self.lead_id = res['result']['CRM_ENTITY_ID']
        self.call_id = res['result']['CALL_ID']

        if self.file:
            self.duration = int(MP3(self.file).info.length)
            self.filename = str(self.file)[len(self.inner_media_path):-len(os.path.splitext(str(self.file))[-1])]

    def my_telephony_externalcall_finish(self, but):
        finish_params = {
            "CALL_ID": self.call_id,
            "USER_ID": self.user_id,
            "DURATION": self.duration,
            "RECORD_URL": f'https://{settings.APP_SETTINGS.app_domain}/media/{self.inner_media_path}{self.filename}.mp3',
            "ADD_TO_CHAT": self.add_to_chat,
        }

        but.call_api_method('telephony.externalcall.finish', finish_params)
