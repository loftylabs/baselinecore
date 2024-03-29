from __future__ import unicode_literals

from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from baselinecore.models.base import BaselinePage

class HomePage(BaselinePage):
    """
    Homepage specific configuration
    """

    template = "index.html"

    snippet = models.CharField(max_length=2502, default="Welcome to Baseline!")

    content_panels = BaselinePage.content_panels + [
        FieldPanel('snippet', classname='title'),
    ]
