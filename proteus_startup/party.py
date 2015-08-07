# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import random
from proteus import Model

from .ir import get_language
from .country import get_country, get_subdivision

__all__ = ['get_party', 'create_party']


def get_party(config, name, no_create=False):
    Party = Model.get('party.party')
    parties = Party.find([('name', '=', name)])
    if parties:
        return parties[0]
    if no_create:
        return
    return create_party(config, name)


def create_party(config, name, lang_code='ca_ES',
        address_name=None, street=None, zip=None, city=None,
        subdivision_code=None, country_code='ES',
        phone=None, website=None,
        account_payable=None, account_receivable=None,
        customer_payment_term=None, supplier_payment_term=None,
        customer_payment_type=None, supplier_payment_type=None,
        sale_price_list=None,
        include_347=True):
    Address = Model.get('party.address')
    ContactMechanism = Model.get('party.contact_mechanism')
    Party = Model.get('party.party')

    parties = Party.find([('name', '=', name)])
    if parties:
        return parties[0]

    country = get_country(config, country_code)
    subdivision = get_subdivision(config, country, subdivision_code,
        no_create=True)

    if zip is None:
        # Create a ZIP from Barcelona if none was provided
        zip = '08' + str(random.randrange(1000)).zfill(3)

    party = Party(name=name)
    party.addresses.pop()
    party.addresses.append(
        Address(
            name=address_name,
            street=street,
            zip=zip,
            city=city,
            country=country,
            subdivision=subdivision))
    if phone:
        party.contact_mechanisms.append(
            ContactMechanism(type='phone',
                value=phone))
    if website:
        party.contact_mechanisms.append(
            ContactMechanism(type='website',
                value=website))
    party.lang = get_language(config, lang_code)

    if account_payable:
        party.account_payable = account_payable
    if account_receivable:
        party.account_receivable = account_receivable

    if hasattr(party, 'customer_payment_term') and customer_payment_term:
        party.customer_payment_term = customer_payment_term
    if hasattr(party, 'supplier_payment_term') and supplier_payment_term:
        party.supplier_payment_term = supplier_payment_term

    if hasattr(party, 'customer_payment_type') and customer_payment_type:
        party.customer_payment_type = customer_payment_type
    if hasattr(party, 'supplier_payment_type') and supplier_payment_type:
        party.supplier_payment_type = supplier_payment_type

    if hasattr(party, 'sale_price_list') and sale_price_list:
        party.sale_price_list = sale_price_list

    if hasattr(party, 'include_347'):
        party.include_347 = include_347

    return party
