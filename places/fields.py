# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.utils.six import with_metaclass
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

from . import Places
from .forms import PlacesField as PlacesFormField


class PlacesField(models.Field):
    description = _("A geoposition field (latitude and longitude)")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(PlacesField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if not value or value == 'None':
            return None
        if isinstance(value, Places):
            return value
        if isinstance(value, list):
            return Places(value[0], value[1], value[2], value[3], value[4])
        # print('getvalue: ', value)
        decimal_parts = [Decimal(val) for val in value.split(';')[-3:-1]]
        # print('value_parts: ', value_parts)
        text_parts = [[val] for val in value.split(';')[:2]]
        # print('text_parts: ', text_parts)

        try:
            latitude = decimal_parts[0]
        except IndexError:
            latitude = '0.0'

        try:
            longitude = decimal_parts[1]
        except IndexError:
            longitude = '0.0'

        try:
            place = ','.join(text_parts[0][0].split(','))
        except Exception:
            pass

        try:
            formatted_address = ','.join(text_parts[1][0].split(','))[1:]
        except Exception:
            pass

        try:
            pincode = value.split(';')[-1]
        except Exception:
            pass

        return Places(place, formatted_address, latitude, longitude, pincode)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_prep_value(self, value):
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': PlacesFormField
        }
        defaults.update(kwargs)
        return super(PlacesField, self).formfield(**defaults)
