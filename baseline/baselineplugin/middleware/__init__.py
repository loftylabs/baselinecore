from baseline.baselineplugin.models import PluginSettings
from baseline.baselineplugin.utils import get_installed_plugins

class PluginSettingsMiddleware(object):

    def process_request(self, request):
        # Patch all of our plugin settings onto the request objects
        plugin_list = [p['package'] for p in get_installed_plugins()]
        settings = PluginSettings.objects.filter(plugin__in=plugin_list)

        request.plugin_settings = {}
        # Dict of plugin_name => dict of settings json
        for s in settings:
            request.plugin_settings[s.plugin] = s.as_object()



