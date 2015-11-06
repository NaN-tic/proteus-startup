# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from .common import create_model
from proteus import Model

__all__ = ['get_country', 'create_country', 'get_subdivision',
    'create_subdivision']


def get_countries(codes):
    Country = Model.get('country.country')
    countries = Country.find([('code', 'in', codes)])
    return {k.code: k for k in countries}


def get_country(country_code):
    Country = Model.get('country.country')
    countries = Country.find([('code', '=', country_code)])
    if countries:
        return countries[0]

    country = create_country(country_code, country_code)
    country.save()
    return country


@create_model('country.country')
def create_country(name, country_code):
    return {
        'name': name,
        'code': country_code,
        }


def get_subdivision(country, subdivision_code, no_create=False):
    Subdivision = Model.get('country.subdivision')
    subdivisions = Subdivision.find([
            ('country', '=', country.id),
            ('code', '=', subdivision_code),
            ])
    if subdivisions:
        return subdivisions[0]

    if no_create:
        return

    subdivision = create_subdivision(country, subdivision_code,
        subdivision_code)
    subdivision.save()
    return subdivision


@create_model('country.subdivision')
def create_subdivision(country, name, subdivision_code):
    return {
        'country': country,
        'name': name,
        'code': subdivision_code,
        }
