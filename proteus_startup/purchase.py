# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model

__all__ = ['create_purchase']


def create_purchase(party, company=None, invoice_address=None,
        shipment_address=None, purchase_date=None, payment_term=None,
        warehouse=None, currency=None):
    Purchase = Model.get('purchase.purchase')

    purchase = Purchase()
    purchase.party = party
    if company:
        purchase.company = company
    if invoice_address:
        purchase.invoice_address = invoice_address
    if shipment_address:
        purchase.shipment_address = shipment_address
    if purchase_date:
        purchase.purchase_date = purchase_date
    if payment_term:
        purchase.payment_term = payment_term
    if warehouse:
        purchase.warehouse
    if currency:
        purchase.currency
    return purchase
