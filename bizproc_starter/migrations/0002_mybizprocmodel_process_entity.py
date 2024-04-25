# Generated by Django 4.2.11 on 2024-04-19 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizproc_starter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mybizprocmodel',
            name='process_entity',
            field=models.CharField(choices=[('UNKNOWN', 'Unknown'), ('COMPANY', 'Company'), ('DEAL', 'Deal'), ('LEAD', 'Lead'), ('CONTACT', 'Contact')], default='UNKNOWN', max_length=7),
        ),
    ]
