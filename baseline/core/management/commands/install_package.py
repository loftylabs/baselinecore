import os
import subprocess
import sys

from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('git_url', nargs='?', type=str)


    def handle(self, *args, **options):
        """
        Installs a package via pip.  To be used by higher level commands for themes and plugins
        """
        subprocess.Popen([
            "pip", "install",  "-e", str(options['git_url'])
        ], env=os.environ.copy()).wait()

