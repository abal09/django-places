from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .widgets import PlacesWidget
from . import Places


class PlacesField(forms.MultiValueField):
    default_error_messages = {
        'invalid': _('Enter a valid geoposition.')
    }

    def __init__(self, *args, **kwargs):
        fields = (
            forms.CharField(label=_('place')),
            forms.CharField(
                label=_('formatted_address'), widget=forms.Textarea()),
            forms.DecimalField(label=_('latitude')),
            forms.DecimalField(label=_('longitude')),
            forms.CharField(label=_('pincode')),
        )
        if 'initial' in kwargs:
            kwargs['initial'] = Places(*kwargs['initial'].split(','))
        self.widget = PlacesWidget()
        super(PlacesField, self).__init__(fields, **kwargs)

    def widget_attrs(self, widget):
        classes = widget.attrs.get('class', '').split()
        classes.append('places')
        return {'class': ' '.join(classes)}

    def compress(self, value_list):
        if value_list:
            return value_list
        return ""
