# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from .common import create_model


__all__ = ['create_asset']


@create_model('asset')
def create_asset(**kwargs):
    pass
