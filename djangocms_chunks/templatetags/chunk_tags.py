# -*- coding: utf-8 -*-
from contextlib import contextmanager

from django import template
from django.utils import six
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from ..models import Chunk


register = template.Library()


@contextmanager
def exceptionless(truth):
    # Accepts one truth parameter, when 'False' normal behavior
    # when 'True' any expection will be suppressed
    try:
        yield
    except Exception:
        if truth:
            # WARNING: suppressing exception
            pass
        else:
            # Reraising exception
            raise


class ChunkFragment(template.Node):
    """
    Get a chunk HTML fragment
    """

    def __init__(self, chunk_id_varname, *args):
        """
        :type insert_instance_varname: string or object
                                       ``django.db.models.Model``
        :param insert_instance_varname: Instance variable name or a string slug
                                        or object id
        """
        self.parse_until = False
        self.chunk_id_varname = template.Variable(chunk_id_varname)
        if args and 'or' in args:
            # We are in a 'parse util' case
            # ALERT: Exceptions will be suppressed to avoid errors from bad
            # tag content
            # Maybe we could analyze more usage case to catch only exceptions
            # related to bad tag content
            self.parse_until = True
            self.nodelist = args[1]

    def render(self, context):
        """
        :type context: object ``django.template.Context``
        :param context: Context tag object

        :rtype: string
        :return: the HTML for the chunk
        """
        # Default assume this is directly an instance
        chunk_instance = self.chunk_id_varname.resolve(context)
        # Assume this is slug
        with exceptionless(self.parse_until):
            if isinstance(chunk_instance, six.string_types):
                chunk_instance = Chunk.objects.get(slug=chunk_instance)
            # Assume this is an id
            elif isinstance(chunk_instance, int):
                chunk_instance = Chunk.objects.get(pk=chunk_instance)

            return mark_safe(self.get_content_render(context,
                                                     chunk_instance))

        # Rely on the fact that manager something went wrong
        # render the fallback template
        return self.nodelist.render(context)

    def get_content_render(self, context, instance):
        """
        Render the chunk HTML, using a template if defined in its instance
        """
        context.update({
            'object': instance,
        })
        [context.update({variable.name: variable.value}) for variable in instance.variable_set.all()]
        try:
            if instance.template:
                context.update({
                    'html': mark_safe(instance.html)
                })
                content = template.loader.render_to_string(
                    instance.template,
                    context.flatten(),
                )
            else:
                t = template.Template(instance.html)
                content = t.render(template.Context(context))
        except template.TemplateDoesNotExist:
            content = _('Template %(template)s does not exist.') % {
                'template': instance.template}
        except Exception as e:
            content = escape(str(e))
            if self.parse_until:
                # In case we are running 'exceptionless'
                # Re-raise exception in order not to get the
                # error rendered
                raise
        return content


@register.tag(name='chunk_fragment')
def do_chunk_fragment(parser, token):
    """
    Display a chunk HTML fragment

    Usage : ::
        {% chunk_fragment [Chunk ID or instance] %}

        {% chunk_fragment [Chunk ID or instance] or %}
            ...This is a fallback...
        {% endchunk_fragment %}
    """
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError(
            'You need to specify at least a "chunk" ID, slug or instance')
    if 'or' in args:
        # Catch contents between tags and pass to renderer
        args.append(parser.parse(('endchunk_fragment',)))
        parser.delete_first_token()
    return ChunkFragment(*args[1:])


do_chunk_fragment.is_safe = True
