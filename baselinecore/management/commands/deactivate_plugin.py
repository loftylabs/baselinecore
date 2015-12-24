import json
import os
import subprocess

from django.conf import settings
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('plugin_name', nargs='?', type=str)

    def handle(self, *args, **options):
        """
        Installs a baselineplugin via pip and selects it.
        """

        # Select it
        old_conf = settings.PLUGIN_CONFIG

        # Make sure it is installed
        if not options['plugin_name'] in old_conf['installed']:
            raise CommandError(
                "plugin {plugin} does not appear to be installed.  \n"
                "plugin options include: \n{valid_plugins}".format(
                    plugin=options['plugin_name'],
                    valid_plugins="\n".join(["  - " + n for n in old_conf['installed']])
                )
            )
        new_conf = old_conf.copy()

        # Dectivate the plugin
        if options['plugin_name'] in new_conf['active']:
            new_conf['active'].remove(options['plugin_name'])

        # Write the new configuration
        with open(os.path.join(settings.BASE_DIR, '.bl-plugin'), 'w') as plugin_conf:
            plugin_conf.write(json.dumps(new_conf))

        # Restart the app
        if settings.DEBUG:
            subprocess.call(['touch', os.path.join(settings.PROJECT_DIR, 'wsgi.py')],
                            env=os.environ.copy())
        else:
            # TODO: Integrate hooks to restart uWSGI
            pass
