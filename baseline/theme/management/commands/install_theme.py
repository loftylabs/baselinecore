import json
import os

from django.core.management import BaseCommand, call_command
from django.conf import settings



class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('git_url', nargs='+', type=str)
        parser.add_argument('name', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        Installs a theme via pip and selects it.
        """
        # Install it
        call_command('install_package', **options)

        # Select it
        old_conf = settings.THEME_CONFIG
        new_conf = old_conf.deepcopy()
        new_conf['installed'] = options['name']

        with open(os.path.join(settings.BASE_DIR, '.bl-theme'), 'w') as theme_conf:
            theme_conf.write(json.dumps(new_conf))
