import json
import os
import subprocess

from django.conf import settings
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('theme_name', nargs='?', type=str)

    def handle(self, *args, **options):
        """
        Installs a baselinetheme via pip and selects it.
        """

        # Select it
        old_conf = settings.THEME_CONFIG

        # Make sure it is installed
        if not options['theme_name'] in old_conf['installed']:
            raise CommandError(
                "Theme {theme} does not appear to be installed.  \n"
                "Theme options include: \n{valid_themes}".format(
                    theme=options['theme_name'],
                    valid_themes="\n".join(["  - " + n for n in old_conf['installed']])
                )
            )
        new_conf = old_conf.copy()

        # Activate the theme
        new_conf['active'] = options['theme_name']

        # Write the new configuration
        with open(os.path.join(settings.BASE_DIR, '.bl-theme'), 'w') as theme_conf:
            theme_conf.write(json.dumps(new_conf))

        # Restart the app
        if settings.DEBUG:
            subprocess.call(['touch', os.path.join(settings.PROJECT_DIR, 'wsgi.py')],
                            env=os.environ.copy())
        else:
            # TODO: Integrate hooks to restart uWSGI
            pass
