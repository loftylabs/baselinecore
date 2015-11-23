import json
import os

from django.core.management import BaseCommand, call_command
from django.conf import settings



class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('git_url', nargs='?', type=str)
        parser.add_argument('name', nargs='?', type=str)

    def handle(self, *args, **options):
        """
        Installs a theme via pip and selects it.
        """
        package_name = options.pop('name')

        # Install it
        call_command('install_package', *[options['git_url']])

        # Select it
        old_conf = settings.THEME_CONFIG
        new_conf = old_conf.copy()

        # Add the new theme (unless it was there already)
        if package_name not in new_conf['installed']:
            new_conf['installed'].append(package_name)

        # Activate the theme
        new_conf['active'] = package_name

        # Write the new configuration
        with open(os.path.join(settings.BASE_DIR, '.bl-theme'), 'w') as theme_conf:
            theme_conf.write(json.dumps(new_conf))
