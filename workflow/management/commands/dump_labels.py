from django.core.management.base import BaseCommand

from workflow.utils import dump_labels


class Command(BaseCommand):
    help = 'Dump configuration models as json'

    def handle(self, *args, **kwargs):
        dump_labels()
