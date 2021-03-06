# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal

import sys

# Weird encoding python2 hack :'(
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

default_app_config = 'places.apps.PlacesConfig'
__version__ = '1.1.8'


class Places(object):

    def __init__(
            self, place, formatted_address, latitude, longitude, pincode):

        if isinstance(latitude, float) or isinstance(latitude, int):
            latitude = str(latitude)
        if isinstance(longitude, float) or isinstance(longitude, int):
            longitude = str(longitude)

        self.place = place
        self.formatted_address = formatted_address
        self.latitude = Decimal(latitude)
        self.longitude = Decimal(longitude)
        self.pincode = pincode

    def __str__(self):
        return "%s; %s; %s; %s; %s" % (
            self.place, self.formatted_address, self.latitude,
            self.longitude, self.pincode)

    def __repr__(self):
        return "Places(%s)" % str(self)

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        return isinstance(other, Places) and self.latitude == \
            other.latitude and self.longitude == other.longitude

    def __ne__(self, other):
        return not isinstance(other, Places) or self.latitude != \
            other.latitude or self.longitude != other.longitude
