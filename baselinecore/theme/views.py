import os
import requests

from django.conf import settings
from django.contrib import messages
from django.core.management import call_command, CommandError
from django.core.urlresolvers import reverse
from django.http import FileResponse
from django.views.generic import TemplateView, RedirectView, View, FormView

from .forms import InstallThemeForm
from .utils import get_installed_themes, get_theme_pkg_meta


MARKETPLACE_API_URL = 'http://market.getbaseline.io/api'


class InstallTheme(FormView):
    """
    Admin view to allow new plugins to be installed via the MarketPlace
    """
    template_name = "baselinecore/theme/install.html"
    form_class = InstallThemeForm

    def get_success_url(self, *args, **kwargs):
        """
        Direct back to the plugin page
        """
        return reverse('wagtailadmin_home')

    def get_context_data(self, **kwargs):

        kwargs.update({
            'installed_themes': get_installed_themes(),
        })

        # query the marketplace to get a list of plugins
        marketplace_plugins = requests.get("{0}/themes/".format(MARKETPLACE_API_URL)).json()
        kwargs['results'] = marketplace_plugins
        return super(InstallTheme, self).get_context_data(**kwargs)

    def form_valid(self, form):
        """
        Install the plugin
        """

        theme_id = form.cleaned_data['theme_id']
        plugin_data = requests.get("{0}/themes/{1}/".format(MARKETPLACE_API_URL,
                                                             theme_id)).json()

        # Github
        if plugin_data['package_type'] == 1:
            try:
                call_command('install_theme',
                             "git+{0}#egg={1}".format(
                                 plugin_data['repo_url'], plugin_data['package_name']),
                             plugin_data['package_name'])
                messages.success(self.request, "Plugin {plugin} was activated successfully.".format(
                    plugin=plugin_data['title']))
            except CommandError:
                messages.error(self.request, "There was an error activating {plugin}.".format(
                    plugin=plugin_data['title']))
        else:
            raise NotImplementedError("Distutil Packages are currently unsupported.")

        return super(InstallTheme, self).form_valid(form)

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
