from django.conf.urls import url
from django.core.urlresolvers import reverse

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem

from baselinecore.plugin.views import ActivatePlugin, DeactivatePlugin, PluginIndex, PluginSettings


@hooks.register('register_admin_menu_item')
def theme_menu():
    return MenuItem('Plugins', reverse('baseline-plugin-index'), classnames='icon icon-cog',
                    order=10000)

@hooks.register('register_admin_urls')
def theme_urls():
    return [
        url(r'^plugins/$', PluginIndex.as_view(), name='baseline-plugin-index'),
        url(r'^plugins/activate/$', ActivatePlugin.as_view(), name='baseline-plugin-activate'),
        url(r'^plugins/deactivate/$', DeactivatePlugin.as_view(), name='baseline-plugin-deactivate'),
        url(r'^plugins/settings/([\d\w_]+)/$', PluginSettings.as_view(), name='baseline-plugin-settings'),
    ]
