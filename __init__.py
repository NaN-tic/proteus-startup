from proteus import config, Model, Wizard

config = config.set_trytond()
config.pool.test = True


def install_module(modules):
    Module = Model.get('ir.module.module')
    contract_module, = Module.find([('name', 'in', modules)])
    Module.install([contract_module.id], config.context)
    Wizard('ir.module.module.install_upgrade').execute('upgrade')
