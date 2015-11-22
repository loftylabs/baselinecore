import subprocess

from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('git_url', nargs='+', type=str)
0
    def handle(self, *args, **options):
        """
        Installs a package via pip.  To be used by higher level commands for themes and plugins
        """
        subprocess.call("pip install -e {url}".format(url=options['git_url']))

