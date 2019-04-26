# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model, Wizard

__all__ = ['install_modules']


def install_modules(modules):
    Module = Model.get('ir.module')

    assert isinstance(modules, (str, list))
    if isinstance(modules, str):
        modules = modules.split(',')

    modules = Module.find([('name', 'in', modules)])
    # 3.6 Module.click(modules, 'install')
    Module.click(modules, 'install')
    Wizard('ir.module.install_upgrade').execute('upgrade')


def close_config_wizard():

    WizardItem = Model.get('ir.module.config_wizard.item')
    for item in WizardItem.find([('state', '=', 'open')]):
        item.state = 'done'
        item.save()
