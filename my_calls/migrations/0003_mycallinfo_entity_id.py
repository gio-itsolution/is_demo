# Generated by Django 4.2.11 on 2024-04-16 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_calls', '0002_rename_callinfo_mycallinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycallinfo',
            name='entity_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
