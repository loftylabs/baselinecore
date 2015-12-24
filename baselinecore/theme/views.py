import os

from django.conf import settings
from django.contrib import messages
from django.core.management import call_command, CommandError
from django.core.urlresolvers import reverse
from django.http import FileResponse
from django.views.generic import TemplateView, RedirectView, View

from .utils import get_installed_themes, get_theme_pkg_meta

class ThemeIndex(TemplateView):
    """
    Admin view to display all themes and allow them to be activated, uninstalled by the user.
    """
    template_name = "baselinecore/theme/theme_index.html"

    def get_context_data(self, **kwargs):
        kwargs.update({
            'installed_themes': get_installed_themes(),
            'active_theme': settings.THEME_CONFIG['active']
        })

        return super(ThemeIndex, self).get_context_data(**kwargs)


class ActivateTheme(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Direct back to the theme page
        """
        return reverse('wagtailadmin_home')

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


class ThemeThumbnail(View):
    """
    Serves a theme's thumbnail image.
    A view to serve images is normally a waste of Django's time, but since only one theme is
    installed at a time we can't take advantage of the staticfiles system here.

    A future feature could collect theme thumbnails into the project's media location when a theme
    is installed...
    """

    def get(self, request, *args, **kwargs):
        # Import the package to find its location on disk.
        theme_package = request.GET.get('theme')
        theme_mod = get_theme_pkg_meta(theme_package)

        path = [os.path.sep] + os.path.dirname(theme_mod.theme.__file__).split(os.path.sep)
        path += ['static', 'thumbnail.png']

        with open(os.path.join(*path), 'r') as thumb_h:
            thumb_image = thumb_h.read()

        return FileResponse(thumb_image, content_type="image/png")
