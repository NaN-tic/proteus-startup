# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from proteus import Model

from .common import create_model
from .account import get_account_expense, get_account_revenue


__all__ = ['get_uom_category', 'get_uom_category_by_xml_id',
    'create_uom_category',
    'get_uom', 'get_uom_by_xml_id', 'create_uom',
    'get_template', 'create_template',
    'get_price_list', 'create_price_list',
    'get_product_attribute', 'create_product_attribute']


def get_uom_category(name):
    Category = Model.get('product.uom.category')
    categories = Category.find([
            ('name', '=', name),
            ])
    if categories:
        return categories[0]
    return create_uom_category(name)


def get_uom_category_by_xml_id(module, fs_id):
    ModelData = Model.get('ir.model.data')
    Category = Model.get('product.uom.category')

    data = ModelData.find([
            ('module', '=', module),
            ('fs_id', '=', fs_id),
            ], limit=1)
    return Category(data[0].db_id)


@create_model('product.uom.category')
def create_uom_category(name):
    return {
        'name': name,
        }


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


@create_model('product.uom')
def create_uom(name, symbol, category, rate=None, rounding=None,
        digits=None):
    values = {
        'name': name,
        'symbol': symbol,
        'category': category,
        }
    if rate is not None:
        values['rate'] = rate
    if rounding is not None:
        values['rounding'] = rounding
    if digits is not None:
        values['digits'] = digits
    return values


def get_template(name, no_create=False):
    ProductTemplate = Model.get('product.template')
    templates = ProductTemplate.find([('name', '=', name)])
    if templates:
        return templates[0]
    if no_create:
        return
    return create_template(name)


@create_model('product.template')
def create_template(**kwargs):
    Template = Model.get('product.template')
    name = kwargs.get('name')
    templates = Template.find(['name', '=', name])
    if templates:
        return templates[0]

    unit = kwargs.get('unit')
    if unit is None:
        unit = get_uom_by_xml_id('product', 'uom_unit')

    values = {
        'name': name,
        }

    # Define Required fields with defaults if not already set.
    for field, default in [
            ('default_uom', get_uom_by_xml_id('product', 'uom_unit')),
            ('list_price', Decimal('10.0')),
            ('cost_price', Decimal('5.45')),
            ('account_expense', get_account_expense()),
            ('account_revenue', get_account_revenue()),
            ]:
        if not field in kwargs:
            values[field] = default
    return values



def get_price_list(name, company):
    PriceList = Model.get('product.price_list')
    price_lists = PriceList.find([
            ('name', '=', name),
            ('company', '=', company.id),
            ])
    if price_lists:
        return price_lists[0]
    return create_price_list(name, company)


@create_model('product.price_list')
def create_price_list(name, company):
    return {
        'name': name,
        'company': company,
        }


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
