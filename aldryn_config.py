# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):
    editor_theme = forms.CharField(
        'Custom editor theme, (e.g. "twilight", default: "github")',
        required=False,
    )
    editor_mode = forms.CharField(
        'Custom editor mode (e.g. "javascript", default: "html")',
        required=False,
    )

    def to_settings(self, data, settings):
        settings['INSTALLED_APPS'].extend(['djangocms_chunks',])
        if data['editor_theme']:
            settings['DJANGOCMS_CHUNKS_THEME'] = data['editor_theme']
        if data['editor_mode']:
            settings['DJANGOCMS_CHUNKS_MODE'] = data['editor_mode']
        return settings
