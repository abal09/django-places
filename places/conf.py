# -*- coding: utf-8 -*-

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured


class AppSettings(object):
    prefix = 'PLACES'
    required_settings = ['MAPS_API_KEY']
    defaults = {
        'MAPS_API_KEY': None,
        'MAP_WIDGET_HEIGHT': 480,
        'MAP_OPTIONS': {},
        'MARKER_OPTIONS': {},
        'USE_JQUERY': True
    }

    def __init__(self, django_settings):
        self.django_settings = django_settings

        for setting in self.required_settings:
            prefixed_name = '%s_%s' % (self.prefix, setting)
            if not hasattr(self.django_settings, prefixed_name):
                raise ImproperlyConfigured(
                    "The '%s' setting is required." % prefixed_name)

    def __getattr__(self, name):
        prefixed_name = '%s_%s' % (self.prefix, name)
        if hasattr(django_settings, prefixed_name):
            return getattr(django_settings, prefixed_name)
        if name in self.defaults:
            return self.defaults[name]
        import pdb
        pdb.set_trace()
        raise AttributeError(
            "'AppSettings' object does not have a '%s' attribute" % name)


settings = AppSettings(django_settings)
