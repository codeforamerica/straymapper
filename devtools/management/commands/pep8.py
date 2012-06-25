import os

from django.core.management.base import BaseCommand

from fabric.api import local


class Command(BaseCommand):
    help = 'Runs pep8 on the entire project'

    def handle(self, *args, **options):
        file_path = os.path.dirname(__file__)
        pep8_cmd = 'find ' + file_path
        pep8_cmd = pep8_cmd + '/../../.. -name "*.py" | xargs pep8 --repeat'
        local(pep8_cmd, capture=False)
