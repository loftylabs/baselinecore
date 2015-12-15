from django.conf import settings


def get_installed_plugins():
    """
    Returns a list of plugin dictionaries containing the package name and the plugin meta info.
    """
    installed_plugins = settings.PLUGIN_CONFIG['installed']

    plugin_list = []
    for plugin_pkg in installed_plugins:
        # Import the plugin and grab its meta info
        plugin_mod = get_plugin_pkg_meta(plugin_pkg)

        plugin_list.append({
            'package': plugin_pkg,
            'meta': plugin_mod.plugin.__plugin_meta__
        })

        # overly cautious...
        del plugin_mod

    return plugin_list


def get_plugin_pkg_meta(pkg):
    mod = __import__(pkg, globals(), locals(), ['plugin'], -1)
    return mod