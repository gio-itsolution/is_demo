from django.db import models
from django.db.utils import IntegrityError


class MyBizprocModel(models.Model):

    class Entity(models.TextChoices):
        UNKNOWN: tuple = 'UNKNOWN', 'Unknown'
        COMPANY: tuple = 'COMPANY', 'Company'
        DEAL: tuple = 'DEAL', 'Deal'
        LEAD: tuple = 'LEAD', 'Lead'
        CONTACT: tuple = 'CONTACT', 'Contact'

    process_id = models.IntegerField(unique=True)
    process_name = models.CharField(max_length=200)
    process_entity = models.CharField(max_length=7, choices=Entity.choices, default=Entity.UNKNOWN)

    @staticmethod
    def find_all_bizprocs(but, method: str) -> None:
        res_bizprocs = but.call_list_method(
            'bizproc.workflow.template.list',
            {'select': ["ID", "NAME"],
             'filter': {'DOCUMENT_TYPE': [
                        'crm',
                        f'CCrmDocument{method.title()}',
                        f'{method}'
                        ]}})

        for item in res_bizprocs:
            MyBizprocModel.objects.update_or_create(
                process_id=item["ID"],
                defaults={'process_name': item['NAME'], 'process_entity': method}
            )

    def run_cur_bizproc(self, but, entity_id, entity) -> None:
        but.call_api_method('bizproc.workflow.start', {
            'TEMPLATE_ID': self.process_id,
            'DOCUMENT_ID': ['crm', f'CCrmDocument{entity.title()}', str(entity_id)]
        })

    def __str__(self):
        return f'Бизнес процесс {self.process_id} - {self.process_name}'

