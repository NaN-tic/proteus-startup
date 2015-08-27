# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from proteus import Model

from .account import get_account_expense, get_account_revenue


__all__ = ['get_uom', 'get_uom_by_xml_id', 'create_uom',
    'get_template', 'create_template',
    'get_price_list', 'create_price_list',
    'get_product_attribute', 'create_product_attribute']


def get_uom(name, category):
    Uom = Model.get('product.uom')
    uoms = Uom.find([
            ('name', '=', name),
            ('category', '=', category.id),
            ])
    if uoms:
        return uoms[0]
    return create_uom(name, name[0], category)


def get_uom_by_xml_id(module, fs_id):
    ModelData = Model.get('ir.model.data')
    Uom = Model.get('product.uom')

    data = ModelData.find([
            ('module', '=', module),
            ('fs_id', '=', fs_id),
            ], limit=1)
    return Uom(data[0].db_id)


def create_uom(name, symbol, category, rate=None, rounding=None,
        digits=None):
    Uom = Model.get('product.uom')
    uom = Uom()
    uom.name = name
    uom.symbol = symbol
    uom.category = category
    if rate is not None:
        uom.rate = rate
    if rounding is not None:
        uom.rounding = rounding
    if digits is not None:
        uom.digits = digits
    return uom


def get_template(name, no_create=False):
    ProductTemplate = Model.get('product.template')
    templates = ProductTemplate.find([('name', '=', name)])
    if templates:
        return templates[0]
    if no_create:
        return
    return create_template(name)


def create_template(**kwargs):

    Template = Model.get('product.template')
    Tax = Model.get('account.tax')

    name = kwargs.get('name')

    templates = Template.find(['name', '=', name])
    if templates:
        return templates[0]

    unit = kwargs.get('unit')
    if unit is None:
        unit = get_uom_by_xml_id('product', 'uom_unit')

    template = Template()
    template.name = name

    for key, value in kwargs.iteritems():
        if key in Template._fields:
            if key in 'customer_taxes' and value:
                for tax in value:
                    template.customer_taxes.append(Tax(tax.id))
                continue
            if key == 'supplier_taxes' and value:
                for tax in value:
                    template.supplier_taxes.append(Tax(tax.id))
                continue

            setattr(template, key, value)

    # Define Required fields with defaults if not already set.

    if 'default_uom' not in kwargs:
        template.default_uom = get_uom_by_xml_id('product', 'uom_unit')

    if 'list_price' not in kwargs:
        template.list_price = Decimal('10.00')

    if 'account_expense' not in kwargs:
        template.account_expense = get_account_expense()

    if 'account_revenue' not in kwargs:
        template.account_revenue = get_account_revenue()

    if 'cost_price' not in kwargs:
        template.cost_price = Decimal('5.45')

    return template



def get_price_list(name, company):
    PriceList = Model.get('product.price_list')
    price_lists = PriceList.find([
            ('name', '=', name),
            ('company', '=', company.id),
            ])
    if price_lists:
        return price_lists[0]
    return create_price_list(name, company)


def create_price_list(name, company):
    ProductPriceList = Model.get('product.price_list')
    product_price_list = ProductPriceList()
    product_price_list.name = name
    product_price_list.company = company
    return product_price_list


def get_product_attribute(name, n_values=None):
    Attribute = Model.get('product.attribute')
    attributes = Attribute.find([('name', '=', name)])
    if attributes:
        return attributes[0]
    return create_product_attribute(name, n_values=n_values)


def create_product_attribute(name, n_values=None):
    Attribute = Model.get('product.attribute')

    attribute = Attribute()
    attribute.name = name
    if n_values:
        for i in range(1, n_values + 1):
            value = attribute.values.new()
            value.sequence = i
            value.name = '%s %s' % (name, i)
            value.code = str(i)
    return attribute
