# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import random
from proteus import Model

from collections import OrderedDict
from .ir import get_language
from .country import get_country, get_subdivision


__all__ = ['create_asset']

 
def create_asset(**kwargs):
    Asset = Model.get('asset')
    asset = Asset()
    for key, value in kwargs.iteritems():
        if key in Asset._fields:
            if not value:
                continue      
            setattr(asset, key, value)
    return asset
    
