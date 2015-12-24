from django import forms
from django.core.exceptions import ImproperlyConfigured

from baselinecore.plugin.models import PluginSettings

class BasePluginSettingsForm(forms.Form):

    plugin = None

    def save(self):
        """
        Saving a plugin settings form updates the PluginSettings record for this plugin
        """

        if self.plugin is None:
            raise ImproperlyConfigured(
                "PluginSettingsForm child classes must define a plugin attribute.")

        plugin_settings, _ = PluginSettings.objects.get_or_create(plugin=self.plugin)
        plugin_settings.set_from_dict(self.cleaned_data)
        plugin_settings.save()
