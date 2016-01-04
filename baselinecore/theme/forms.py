from django import forms


class InstallThemeForm(forms.Form):
    theme_id = forms.UUIDField()