from django.core.management.base import BaseCommand

from workflow.utils import dump_configurations


class Command(BaseCommand):
    help = 'Dump configuration models as json'

    def handle(self, *args, **kwargs):
        dump_configurations()
