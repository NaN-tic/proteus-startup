# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model
from .common import create_model


__all__ = ['get_party', 'create_party', 'create_address',
    'create_contact_mechanism', 'get_parties_by_code']


@create_model('party.contact_mechanism')
def create_contact_mechanism(**kwargs):
    pass


@create_model('party.address')
def create_address(**kwargs):
    pass


@create_model('party.party')
def create_party(**kwargs):
    pass


def get_party(name, no_create=False):
    Party = Model.get('party.party')
    parties = Party.find([('name', '=', name)])
    if parties:
        return parties[0]
    if no_create:
        return
    return create_party(name=name)


def get_parties_by_code():
    Party = Model.get('party.party')
    return dict((p.code, p) for p in Party.find([]))
