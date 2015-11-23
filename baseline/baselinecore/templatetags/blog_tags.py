from django import template

from baseline.baselinecore.models import BlogPage

register = template.Library()

@register.simple_tag(takes_context=True)
def get_latest_posts(context):
    context.update(
        {'latest_blog_posts': BlogPage.objects.live().order_by('-datetime')[:5]}
    )

    return ""
