# copyright notices and license terms.
from decimal import Decimal
from proteus import Model

__all__ = ['supplier_location', 'storage_location', 'customer_location',
    'lost_found_location', 'make_inventory']


def supplier_location():
    Location = Model.get('stock.location')
    supplier_loc, = Location.find([('code', '=', 'SUP')])
    return supplier_loc


def storage_location():
    Location = Model.get('stock.location')
    storage_loc, = Location.find([('code', '=', 'STO')])
    return storage_loc


def customer_location():
    Location = Model.get('stock.location')
    customer_loc, = Location.find([('code', '=', 'CUS')])
    return customer_location


def lost_found_location():
    Location = Model.get('stock.location')
    lost_found, = Location.find([('code', '=', 'CUS')])
    return lost_found


def make_inventory(**kwargs):

    storage_loc = kwargs.get('storage_location')

    Inventory = Model.get('stock.inventory')
    inventory = Inventory()
    inventory.location = storage_loc
    inventory.save()

    lines = kwargs.get('lines')

    for prod, lot, qty in lines:
        l = inventory.lines.new()
        l.product = prod
        l.lot = lot
        l.quantity = qty

    inventory.save()
    inventory.click('confirm')
