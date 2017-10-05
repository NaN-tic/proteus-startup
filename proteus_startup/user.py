# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model
from .common import create_model

__all__ = ['reload_context', 'change_user_company', 'get_user']


def reload_context(config):
    User = Model.get('res.user')
    config._context = User.get_preferences(True, config.context)


def change_user_company(config, user, new_company, main_company=None):
    user.main_company = main_company if main_company else new_company
    user.company = new_company
    user.save()
    reload_context(config)
    # Ensure company is loaded on context
    config._context.update({'company': new_company.id})


def get_user(login, name, **kargs):
    User = Model.get('res.user')

    domain = [
        ('login', '=', login),
        ]
    users = User.find(domain)
    if users:
        return users[0]
    return create_user(login, name, **kargs)


@create_model('res.user')
def create_user(login, name, **kargs):
    values = {
        'login': login,
        'name': name,
        }

    if 'main_company' in kargs:
        values['company'] = kargs['main_company']
    return values
