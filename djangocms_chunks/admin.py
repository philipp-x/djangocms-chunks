# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings
from django.db import models
from django.forms import Textarea

from .models import Chunk, Variable

# Register your models here.


class VariableInline(admin.TabularInline):
    model = Variable
    extra = 0


class ChunkAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    search_fields = ['slug', 'name']
    prepopulated_fields = {'slug': ('name',)}
    change_form_template = 'djangocms_chunks/admin/change_form.html'
    text_area_attrs = {
        'rows': 20,
        'data-editor': True,
        'data-theme': getattr(settings, 'DJANGOCMS_CHUNKS_THEME', 'twilight'),
        'data-mode': getattr(settings, 'DJANGOCMS_CHUNKS_MODE', 'html'),
    }

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs=text_area_attrs)}
    }

    inlines = (VariableInline,)


admin.site.register(Chunk, ChunkAdmin)
