from django.core.management.base import BaseCommand

from workflow.models import Qualification
from workflow.services.mturk import MTurkConnection


class Command(BaseCommand):
    help = 'Create Qualifications on Amazon MTurk'

    def handle(self, *args, **kwargs):  # noqa
        mturk = MTurkConnection()
        response = mturk.client.list_qualification_types(
            Query='CSMR-Labeling',
            MustBeRequestable=True,
            MustBeOwnedByCaller=True,
            MaxResults=20
        )
        print(response['QualificationTypes'])
        for q in response['QualificationTypes']:
            Qualification.objects.get_or_create(
                name=q['Name'],
                defaults={
                    'mturk_id': q['QualificationTypeId']
                }
            )
