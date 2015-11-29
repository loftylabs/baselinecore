import time

from django.conf import settings
from django.contrib import messages
from django.core.management import call_command, CommandError
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView


class ThemeIndex(TemplateView):
    """
    Admin view to display all themes and allow them to be activated, uninstalled by the user.
    """
    template_name = "baselinetheme/theme_index.html"

    def get_context_data(self, **kwargs):
        kwargs.update({
            'installed_themes': settings.THEME_CONFIG['installed'],
            'active_theme': settings.THEME_CONFIG['active']
        })

        return super(ThemeIndex, self).get_context_data(**kwargs)


class ActivateTheme(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Direct back to the theme page
        """
        return reverse('baseline-theme-index')

    def get(self, request, *args, **kwargs):
        """
        Activate the selected theme.
        """
        theme = request.GET.get('theme')
        try:
            call_command('select_theme', *[theme])
            messages.success(request, "Theme {theme} was activated successfully.".format(
                theme=theme))
        except CommandError:
            messages.error(request, "There was an error activating {theme}.".format(
                theme=theme))

        return super(ActivateTheme, self).get(request, *args, **kwargs)
