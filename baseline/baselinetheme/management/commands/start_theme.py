from django.core.management import BaseCommand


DEFAULT_THEME = 'baseline.baselinetheme.baseline2015'

class Command(BaseCommand):

    def handle(self):
        """
        Start a new baselinetheme based on the default baselinetheme package.
        """
        pass