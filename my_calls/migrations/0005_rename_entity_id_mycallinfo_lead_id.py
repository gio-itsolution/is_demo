# Generated by Django 4.2.11 on 2024-04-16 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_calls', '0004_alter_mycallinfo_entity_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mycallinfo',
            old_name='entity_id',
            new_name='lead_id',
        ),
    ]
