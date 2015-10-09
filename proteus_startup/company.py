# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model, Wizard

__all__ = ['create_company']


# TODO: add default timezone='Europe/Madrid'?
def create_company(party, currency, timezone=None, parent=None):
    Company = Model.get('company.company')

    existing_company_ids = [c.id for c in Company.find([])]

    company_config = Wizard('company.company.config')
    company_config.execute('company')
    company_config.form.party = party
    company_config.form.currency = currency
    if parent:
        company_config.form.parent = parent
    if timezone:
        company_config.form.timezone = timezone
    company_config.execute('add')

    domain = []
    if existing_company_ids:
        company, = Company.find([
                ('id', 'not in', existing_company_ids),
                ])
    else:
        company, = Company.find([])
    return company
