# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model

__all__ = ['get_country', 'create_country', 'get_subdivision',
    'create_subdivision']


def get_country(config, country_code):
    Country = Model.get('country.country')
    countries = Country.find([('code', '=', country_code)])
    if countries:
        return countries[0]

    country = create_country(config, country_code, country_code)
    country.save()
    return country


def create_country(config, name, country_code):
    Country = Model.get('country.country')
    country = Country()
    country.name = name
    country.code = country_code
    return country


def get_subdivision(config, country, subdivision_code, no_create=False):
    Subdivision = Model.get('country.subdivision')
    subdivisions = Subdivision.find([
            ('country', '=', country.id),
            ('code', '=', subdivision_code),
            ])
    if subdivisions:
        return subdivisions[0]

    if no_create:
        return

    subdivision = create_subdivision(config, country, subdivision_code,
        subdivision_code)
    subdivision.save()
    return subdivision


def create_subdivision(config, country, name, subdivision_code):
    Subdivision = Model.get('country.subdivision')
    subdivision = Subdivision()
    subdivision.country = country
    subdivision.name = name
    subdivision.code = subdivision_code
    return subdivision
