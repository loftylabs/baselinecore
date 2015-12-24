import json

from django.db import models


class PluginSettings(models.Model):
    """
    Stores JSON data for plugin settings.
    """

    plugin = models.CharField(max_length=64)
    json = models.TextField(default="{}")

    def as_object(self):
        return json.loads(self.json)

    def set_from_dict(self, settings):
        self.json = json.dumps(settings)
