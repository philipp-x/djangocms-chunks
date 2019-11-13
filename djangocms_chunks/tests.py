# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory

from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer

from .models import Chunk, Variable
from .cms_plugins import ChunkPlugin

# Create your tests here.


class ChunkTestCase(TestCase):

    def setUp(self):
        self.language = 'en'
        self.chunk = Chunk.objects.create(name='Chunk', slug='chunk', html='<p>Hello, {{ variable }}!</p>')
        self.variable = Variable.objects.create(chunk=self.chunk, name='variable', value='World')

    def tearDown(self):
        self.chunk.delete()
        self.variable.delete()

    def test_chunk_instance(self):
        """Chunk instance has been created"""
        chunk = Chunk.objects.get(slug='chunk')
        variable = chunk.variable_set.all()[0]
        self.assertEqual(chunk.name, 'Chunk')
        self.assertEqual(variable.value, 'World')

    def test_chunk_plugin(self):
        """Chunk plugin has been created"""
        chunk = Chunk.objects.get(slug='chunk')
        placeholder = Placeholder.objects.create(slot='content')
        model_instance = add_plugin(
            placeholder,
            ChunkPlugin,
            self.language,
            chunk=chunk,
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {}).replace('\n', '')
        self.assertEqual(html, '<p>Hello, World!</p>')
