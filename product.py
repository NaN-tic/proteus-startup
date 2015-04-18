from proteus import Model
from account import *

ProductUom = Model.get('product.uom')
ProductTemplate = Model.get('product.template')
Product = Model.get('product.product')


def unit(name):
    unit, = ProductUom.find([('name', '=', name)])
    return unit


def template(name):

    templates = ProductTemplate.find(['name', '=', name])
    if templates:
        return templates[0]

    template = ProductTemplate()
    template.name = name
    template.default_uom = unit
    template.type = 'service'
    template.list_price = Decimal('40')
    template.cost_price = Decimal('25')
    template.account_expense = account_expense()
    template.account_revenue = account_revenue()
    template.customer_taxes.append(tax)

    return template
