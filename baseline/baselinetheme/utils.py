from django.conf import settings


def get_installed_themes():
    """
    Returns a list of theme dictionaries containing the package name and the theme meta info.
    """
    installed_themes = settings.THEME_CONFIG['installed']

    theme_list = []
    for theme_pkg in installed_themes:
        # Import the theme and grab its meta info
        theme_mod = get_theme_pkg_meta(theme_pkg)

        theme_list.append({
            'package': theme_pkg,
            'meta': theme_mod.theme.__theme_meta__
        })

        # overly cautious...
        del theme_mod

    return theme_list


def get_theme_pkg_meta(pkg):
    mod = __import__(pkg, globals(), locals(), ['theme'], -1)
    return mod