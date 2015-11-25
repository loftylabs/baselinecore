from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from baseline.baselinecore.models import BaselinePage

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('baselinecore.BlogPage', related_name='tagged_items')


class BlogPage(Page):

    class Meta:
        verbose_name = "Blog Post"

    datetime = models.DateTimeField("Post Date/Time")
    snippet = models.CharField(max_length=250)
    primary_image =  models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
    ])

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('datetime'),
        FieldPanel('snippet'),
        ImageChooserPanel('primary_image'),
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]


class BlogIndexPage(BaselinePage):

    class Meta:
        verbose_name = "Blog Index"

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    @property
    def blog_posts(self):
        return BlogPage.objects.live().descendant_of(self).order_by('-datetime')

    @property
    def recent_blog_posts(self):
        return self.blog_posts[:5]
