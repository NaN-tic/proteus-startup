# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from .common import create_model

__all__ = ['create_purchase']


@create_model('purchase.purchase')
def create_purchase(**kargs):
    assert 'party' in kargs, 'A party is required'
