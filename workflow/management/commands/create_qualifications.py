import logging

from django.core.management.base import BaseCommand, CommandError

from workflow.models import Qualification
from workflow.services.mturk import MTurkConnection

def create_or_update_credential(mturk, cfg, cred_name):
    try:
        id = mturk.create_qualification(cfg)
        Qualification.objects. \
            update_or_create(name=cred_name,
                             defaults={'mturk_id': id})
    except Exception as e:
        print(e)
        logging.error(f"Failed to create credential {cred_name}. "
                      f"Error message {e}.")

class Command(BaseCommand):
    help = 'Create Qualifications on Amazon MTurk and add to Database'

    def handle(self, *args, **kwargs):  # noqa
        try:
            mturk = MTurkConnection()
            cred_name = 'CSMR-Labeling-qualification-complete'
            cfg = {
                'Name': cred_name,
                'Description': cred_name,
                'QualificationTypeStatus': 'Active',
            }
            create_or_update_credential(mturk, cfg, cred_name)
            for i in range(1, 10):
               for let in ['A', 'B']:
                    cred_name = f'CSMR-Labeling-{i}{let}'
                    cfg = {
                        'Name': cred_name,
                        'Description': f'CSMR-Labeling Worker Group {i}{let}',
                        'QualificationTypeStatus': 'Active'
                    }
                    create_or_update_credential(mturk, cfg, cred_name)
        except IOError:
            raise CommandError()
