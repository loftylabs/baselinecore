from __future__ import unicode_literals


from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel


class BaselinePage(Page):
    """
    Core type for static pages.  Abstract so that an additional layer of inheritance is not added
    between wagtail's base page and child pages.
    """
    is_creatable = False

    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    class Meta:
        abstract = True


class StaticPage(BaselinePage):

    template = "page.html"