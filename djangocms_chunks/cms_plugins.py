# -*- coding: utf-8 -*-
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template import Context
from django.conf import settings

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import ChunkPtr


CACHE_ENABLED = getattr(settings, 'DJANGOCMS_CHUNKS_CACHE', True)


class ChunkPlugin(CMSPluginBase):
    model = ChunkPtr
    name = _('Chunk')
    render_template = 'djangocms_chunks/chunk.html'
    text_enabled = True
    text_editor_preview = False
    cache = CACHE_ENABLED

    def render(self, plugin_context, instance, placeholder):
        context = plugin_context.flatten()
        [context.update({variable.name: variable.value}) for variable in instance.chunk.variable_set.all()]
        try:
            if instance.chunk.template:
                t = template.loader.get_template(instance.chunk.template)
                context.update({
                    'html': mark_safe(instance.chunk.html)
                })
                content = t.render(context)
            else:
                t = template.Template(instance.chunk.html)
                content = t.render(Context(context))
        except template.TemplateDoesNotExist:
            content = _('Template %(template)s does not exist.') % {
                'template': instance.chunk.template}
        except Exception as e:
            content = escape(str(e))
        plugin_context.update({
            'placeholder': placeholder,
            'object': instance,
            'html': mark_safe(instance.chunk.html),
            'content': content,
        })
        return plugin_context


plugin_pool.register_plugin(ChunkPlugin)
