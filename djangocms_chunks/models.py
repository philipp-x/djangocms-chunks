# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from cms.utils.compat.dj import python_2_unicode_compatible

# Create your models here.


# Stores the actual data
@python_2_unicode_compatible
class Chunk(models.Model):
    """
    A chunk of HTML or a Django template
    """
    name = models.CharField(
        verbose_name=_('Name'),
        unique=True,
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        unique=True,
        blank=False,
        default='',
        max_length=255,
    )
    html = models.TextField(
        verbose_name=_('HTML'),
        blank=True,
    )
    template = models.CharField(
        verbose_name=_('Template'),
        blank=True,
        max_length=255,
        help_text=_('Enter a template to be rendered. If field TEMPLATE '
                    'is given, the content of field HTML will be passed '
                    'as template variable {{ html }} to the template. '
                    'Otherwise, the content of field HTML is rendered.'),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Chunk')
        verbose_name_plural = _('Chunks')


# Variable model
class Variable(models.Model):
    """
    A Django template variable
    """
    chunk = models.ForeignKey(
        Chunk,
        verbose_name=_('Chunk')
    )
    name = models.SlugField(
        verbose_name=_('Name'),
        unique=True
    )
    value = models.CharField(
        verbose_name=_('Value'),
        max_length=255
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Variable')
        verbose_name_plural = _('Variables')


# Plugin model - just a pointer to Chunk
@python_2_unicode_compatible
class ChunkPtr(CMSPlugin):
    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
        on_delete=models.CASCADE,
    )

    chunk = models.ForeignKey(Chunk, on_delete=models.CASCADE,)

    class Meta:
        verbose_name = _('Chunk Ptr')
        verbose_name_plural = _('Chunk Ptrs')

    def __str__(self):
        # Return the referenced chunk's name rather than the default (ID #)
        return self.chunk.name
