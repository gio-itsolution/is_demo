from django.contrib import admin
from .models import MyCallInfo


@admin.register(MyCallInfo)
class MyCallInfoAdmin(admin.ModelAdmin):
    list_display = ('user_phone', 'user_id', 'phone_number', 'call_date',
                    'type', 'duration', 'add_to_chat', 'call_id', 'file',
                    'lead_id')

