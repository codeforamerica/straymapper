from django.core.management.base import BaseCommand, CommandError

from fabric.api import local


class Command(BaseCommand):
    help = 'Runs pep8 on the entire project'

    def handle(self, *args, **options):
        local('find ../straymapper -name "*.py" | xargs pep8 --repeat',
            capture=False)
