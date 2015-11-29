from django.conf.urls import url
from django.core.urlresolvers import reverse

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem

from baseline.baselinetheme.views import ActivateTheme, ThemeIndex, ThemeThumbnail


@hooks.register('register_admin_menu_item')
def theme_menu():
    return MenuItem('Themes', reverse('baseline-theme-index'), classnames='icon icon-edit',
                    order=10000)

@hooks.register('register_admin_urls')
def theme_urls():
    return [
        url(r'^themes/$', ThemeIndex.as_view(), name='baseline-theme-index'),
        url(r'^themes/activate/$', ActivateTheme.as_view(), name='baseline-theme-activate'),
        url(r'^themes/thumb/$', ThemeThumbnail.as_view(), name='baseline-theme-thumb'),
    ]
