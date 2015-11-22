from django.core.management import BaseCommand


DEFAULT_THEME = 'baseline.theme.baseline2015'

class Command(BaseCommand):

    def handle(self):
        """
        Start a new theme based on the default theme package.
        """
        pass