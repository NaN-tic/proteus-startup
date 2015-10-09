# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model

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
    config._context.update({'company': new_company.id,})


def get_user(login, name, password=None, language=None, signature=None,
        email=None, menu=None, main_company=None, company=None):
    User = Model.get('res.user')

    domain = [
        ('login', '=', login),
        ]
    if main_company:
        domain.append(('main_company', '=', main_company.id))
    users = User.find(domain)
    if users:
        return users[0]
    return create_user(login, name, password=password, language=language,
        signature=signature, email=email, menu=menu)


def create_user(login, name, password=None, language=None, signature=None,
        email=None, menu=None, main_company=None, company=None):
    User = Model.get('res.user')

    user = User()
    user.login = login
    user.name = name
    if password:
        user.password = password
    if language:
        user.language = language
    if signature:
        user.signature = signature
    if email:
        user.email = email
    if menu:
        user.menu = menu
    if main_company:
        user.main_company
        if company:
            user.company = company
        else:
            user.company = main_company
    return user
