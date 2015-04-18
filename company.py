from proteus import config, Model, Wizard

Company = Model.get('company.company')
Party = Model.get('party.party')


def create_company(party, currency):
    company_config = Wizard('company.company.config')
    company_config.execute('company')
    company = company_config.form
    company.party = party
    company.currency = currency
    company_config.execute('add')
    company, = Company.find([])
    return company


