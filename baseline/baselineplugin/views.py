import os
import urllib

from django.conf import settings
from django.contrib import messages
from django.core.management import call_command, CommandError
from django.core.urlresolvers import reverse
from django.http import FileResponse
from django.views.generic import TemplateView, RedirectView, View

from .utils import get_installed_plugins, get_plugin_pkg_meta

class PluginIndex(TemplateView):
    """
    Admin view to display all plugins and allow them to be activated, uninstalled by the user.
    """
    template_name = "baselineplugin/plugin_index.html"

    def get_context_data(self, **kwargs):

        # Mark which plugins are active
        plugins = get_installed_plugins()
        for p in plugins:
            if p['package'] in settings.PLUGIN_CONFIG['active']:
                p['is_active'] = True

        kwargs.update({
            'installed_plugins': plugins,
        })

        return super(PluginIndex, self).get_context_data(**kwargs)


class ActivatePlugin(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Direct back to the plugin page
        """
        return reverse('wagtailadmin_home')

    def get(self, request, *args, **kwargs):
        """
        Activate the selected plugin.
        """
        plugin = request.GET.get('plugin')
        try:
            call_command('activate_plugin', *[plugin])
            messages.success(request, "Plugin {plugin} was activated successfully.".format(
                plugin=plugin))
        except CommandError:
            messages.error(request, "There was an error activating {plugin}.".format(
                plugin=plugin))

        return super(ActivatePlugin, self).get(request, *args, **kwargs)


class DeactivatePlugin(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Direct back to the plugin page
        """
        return reverse('wagtailadmin_home')

    def get(self, request, *args, **kwargs):
        """
        Activate the selected plugin.
        """
        plugin = request.GET.get('plugin')
        try:
            call_command('deactivate_plugin', *[plugin])
            messages.success(request, "Plugin {plugin} was deactivated successfully.".format(
                plugin=plugin))
        except CommandError:
            messages.error(request, "There was an error deactivating {plugin}.".format(
                plugin=plugin))

        return super(DeactivatePlugin, self).get(request, *args, **kwargs)
