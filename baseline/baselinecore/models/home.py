from __future__ import unicode_literals

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel

class HomePage(Page):

    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
