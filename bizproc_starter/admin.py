from django.contrib import admin
from .models import MyBizprocModel


@admin.register(MyBizprocModel)
class MyBizprocAdmin(admin.ModelAdmin):
    list_display = ('process_id', 'process_name', 'process_entity')