# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model, Wizard

__all__ = ['install_modules']


def install_modules(config, modules):
    Module = Model.get('ir.module.module')

    assert isinstance(modules, (basestring, list))
    if isinstance(modules, basestring):
        modules = modules.split(',')

    modules = Module.find([('name', 'in', modules)])
    # 3.6 Module.click(modules, 'install')
    Module.install([m.id for m in modules], config.context)
    Wizard('ir.module.module.install_upgrade').execute('upgrade')
