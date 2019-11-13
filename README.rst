=================
django CMS Chunks
=================

**django CMS Chunks** provides a plugin for `django CMS <http://django-cms.org>`_ to inject HTML, CSS or JavaScript chunks into your website. This addon comes also with support for custom `Template Variables <https://docs.djangoproject.com/en/2.2/topics/templates/#variables>`_.

This addon is compatible with `Divio Cloud <http://divio.com>`_.

We recommend using this plugin only during development::

    This plugin is a potential security hazard, since it allows authorized-
    users to place custom markup or Javascript on pages bypassing all of
    Django's normal sanitization mechanisms. This could be exploited by users
    with the right to add chunks to elevate their privileges to superusers.
    This plugin should only be used during the initial development phase for
    rapid prototyping and testing.


Documentation
=============

Requirements
------------

See ``REQUIREMENTS`` in the `setup.py <https://github.com/philipp-x/djangocms-chunks/blob/master/setup.py>`_ file for additional dependencies.

* Python 2.7, 3.4 or higher
* Django 1.11 or higher
* django CMS 3.4 or higher


Installation
------------

For a manual install, follow the steps below.

1. Run ``pip install https://github.com/philipp-x/djangocms-chunks/archive/1.0.0.tar.gz#egg=djangocms-chunks``
2. Add ``djangocms_chunks`` to your ``INSTALLED_APPS``
3. Run ``python manage.py migrate djangocms_chunks``

Copy ``addon.json``, ``aldryn_config.py`` and ``settings.json`` from the addon into the ``addons`` directory within your project if you are using `Divio Cloud <http://divio.com>`_.


Configuration
-------------

We are using `Ace <https://ace.c9.io/>`_ as our editor of choice to edit the chunk content. You can customize the `theme <https://github.com/ajaxorg/ace/tree/master/lib/ace/theme>`_ and `mode <https://github.com/ajaxorg/ace/tree/master/lib/ace/mode>`_ through::

    DJANGOCMS_CHUNKS_THEME = 'twilight'
    DJANGOCMS_CHUNKS_MODE = 'html'


Normally all plugins will be cached. Set ``DJANGOCMS_CHUNKS_CACHE`` to ``False`` if your chunk displays dynamic content, e.g. ``{% show_menu ... %}``::

    DJANGOCMS_CHUNKS_CACHE = False


Template tag
------------

You can also use a template tag to render a chunk rather than a plugin::

    {% load chunk_tags %}
    {% chunk_fragment [reference] %}


Replace ``[reference]`` with either:

* The chunk ID, e.g. ``{% chunk_fragment 42 %}``
* The chunk slug, e.g. ``{% chunk_fragment 'my-chunk' %}``
* The chunk instance, e.g. ``{% chunk_fragment instance.chunk %}``

Optionally provide a fallback if there is no matching id/slug/instance::

    {% chunk_fragment 'my-chunk' or %}
        ... your content fallback here ...
    {% endchunk_fragment %}


Running Tests
-------------

You can run tests by executing::

    python manage.py test djangocms_chunks.tests


