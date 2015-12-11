from django.conf import settings
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

    template = 'blog/post.html'

    class Meta:
        verbose_name = "Blog Post"

    # TODO:  Probably make this non-nullable in the production version
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                               on_delete=models.SET_NULL)

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
        FieldPanel('snippet'),
        FieldPanel('datetime'),
        FieldPanel('author'),
        ImageChooserPanel('primary_image'),
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

    @property
    def author_name(self):
        """
        Default to username if no first/last name are provided
        """
        if self.author:

            if self.author.get_full_name() != "":
                return self.author.get_full_name()
            else:
                return self.author.username


class BlogIndexPage(BaselinePage):

    template = 'blog/index.html'

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
