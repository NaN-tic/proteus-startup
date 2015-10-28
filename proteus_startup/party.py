# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import random
from proteus import Model

from collections import OrderedDict
from .ir import get_language
from .country import get_country, get_subdivision


__all__ = ['get_party', 'create_party', 'create_address', 'create_contact_mechanism']



def create_contact_mechanism(**kwargs):
    Contact = Model.get('party.contact.mechanism')
    contact = Contact()
    for key, value in kwargs.iteritems():        
        if key in Contact._fields:
            if not value:
                continue      
            setattr(contact, key, value)
    return contact
    


def create_address(**kwargs):
    Address = Model.get('party.address')
    address = Address()
    for key, value in kwargs.iteritems():        
        if key in Address._fields:
            if not value:
                continue      
                setattr(address, key, value)
    return address
    

def create_party(**kwargs):
    
    Party = Model.get('party.party')
    party = Party()
    for key, value in kwargs.iteritems():        
        if key in Party._fields:
            if not value:
                continue
                        
            setattr(party, key, value)
    return party
    

def get_party(name, no_create=False):
    Party = Model.get('party.party')
    parties = Party.find([('name', '=', name)])
    if parties:
        return parties[0]
    if no_create:
        return
    return create_party(name)


