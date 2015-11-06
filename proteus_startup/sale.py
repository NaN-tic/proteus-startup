# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from .common import create_model
from proteus import Model

__all__ = ['create_sale_shop', 'create_sale']


@create_model('sale.shop')
def create_sale_shop(**kwargs):
    values = {}

    def get_sequence():
        Sequence = Model.get('ir.sequence')
        sale_sequence, = Sequence.find([
            ('code', '=', 'sale.sale'),
        ])

    for field, default in [
            ('sale_shipment_method', 'order'),
            ('sale_invoice_method', 'order'),
            ('sale_sequence', get_sequence()),
            ]:
        if field not in kwargs:
            values[field] = default
    return values


@create_model('sale.sale')
def create_sale(**kargs):
    assert 'party' in kargs, 'A party is required'
