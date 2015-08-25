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


def create_template(name, type='goods', unit=None, list_price=None,
        cost_price=None, salable=False, purchasable=False,
        account_expense=None, account_revenue=None,
        customer_taxes=None, supplier_taxes=None):
    Template = Model.get('product.template')
    Tax = Model.get('account.tax')

    templates = Template.find(['name', '=', name])
    if templates:
        return templates[0]

    if unit is None:
        unit = get_uom_by_xml_id('product', 'uom_unit')

    template = Template()
    template.name = name
    template.type = type
    template.default_uom = unit
    template.list_price = (list_price if list_price is not None
        else Decimal('40'))
    template.cost_price = (cost_price if cost_price is not None
        else Decimal('25'))
    # if salable and 'hasattr(Template, 'salable'):
    if salable and 'salable' in Template._fields:
        template.salable = True
    # if purchasable and hasattr(Template, 'purchasable'):
    if purchasable and 'purchasable' in Template._fields:
        template.purchasable = True
    template.account_expense = (account_expense if account_expense is not None
        else get_account_expense())
    template.account_revenue = (account_revenue if account_revenue is not None
        else get_account_revenue())
    if customer_taxes:
        for tax in customer_taxes:
            template.customer_taxes.append(Tax(tax.id))
    if supplier_taxes:
        for tax in supplier_taxes:
            template.supplier_taxes.append(Tax(tax.id))

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
