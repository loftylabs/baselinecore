import json
import os


DEFAULT_THEME_CONFIG = {
    'active': 'baseline.baselinetheme.baseline2015',
    'installed': ['baseline.baselinetheme.baseline2015']
}

DEFAULT_PLUGIN_CONFIG = {
    'active': [],
    'installed': [],
}


def get_pluggable_config(base_directory):
    """
    Reads installed/active themes and plugins from baseline configuration files.
    Returns a tuple for THEME_CONFIG and PLUGIN_CONFIG settings.
    """

    try:
        with open(os.path.join(base_directory, '.bl-theme'), 'r') as theme_config_handler:
            theme_config = json.loads(str(theme_config_handler.read()))
    except IOError:
        theme_config = DEFAULT_THEME_CONFIG

    try:
        with open(os.path.join(base_directory, '.bl-plugin'), 'r') as plugin_config_handler:
            plugin_config = json.loads(plugin_config_handler.read())
    except IOError:
        plugin_config = DEFAULT_PLUGIN_CONFIG

    return theme_config, plugin_config

def get_patched_apps(themes, plugins, apps):
    """
    Patches in the active themes and plugins to the installed apps list provided by settings.py
    """
    return plugins['active'] + [
        # Theme first so it has template priority!
        themes['active']
    ] + apps