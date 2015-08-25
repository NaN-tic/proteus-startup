# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model

__all__ = ['create_sale_shop', 'create_sale']


def create_sale_shop(name, company, warehouse, currency, price_list,
              payment_term, sale_invoice_method='order',
              sale_shipment_method='order', sale_sequence=None, address=None,
              users=None):
    Sequence = Model.get('ir.sequence')
    Shop = Model.get('sale.shop')
    User = Model.get('res.user')

    shop = Shop()
    shop.name = name
    shop.company = company
    shop.warehouse = warehouse
    shop.currency = currency
    shop.price_list = price_list
    shop.payment_term = payment_term
    shop.sale_invoice_method = sale_invoice_method
    shop.sale_shipment_method = sale_shipment_method

    if sale_sequence is None:
        sale_sequence, = Sequence.find([
            ('code', '=', 'sale.sale'),
        ])
    shop.sale_sequence = sale_sequence

    if address:
        shop.address = address

    if users:
        for user in users:
            shop.users.pappend(User(user.id))
    return shop


def create_sale(party, shop=None, company=None, invoice_address=None,
        shipment_address=None, payment_term=None, warehouse=None,
        currency=None):
    Sale = Model.get('sale.sale')

    sale = Sale()
    sale.party = party
    # if shop and hasattr(Sale, 'shop'):
    if shop and 'shop' in Sale._fields:
        sale.shop = shop
    if company:
        sale.company = company
    if invoice_address:
        sale.invoice_address = invoice_address
    if shipment_address:
        sale.shipment_address = shipment_address
    if payment_term:
        sale.payment_term = payment_term
    if warehouse:
        sale.warehouse
    if currency:
        sale.currency
    return sale
