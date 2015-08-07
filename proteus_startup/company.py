# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model, Wizard

__all__ = ['create_company']


def create_company(config, party, currency):
    Company = Model.get('company.company')

    company_config = Wizard('company.company.config')
    company_config.execute('company')
    company_config.form.party = party
    company_config.form.currency = currency
    company_config.execute('add')
    company, = Company.find([])
    return company
