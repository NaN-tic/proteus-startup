# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import config as pconfig
import os
__all__ = ['init_database', 'drop_database', 'connect_database']


def init_database():

    from trytond.tests.test_tryton import drop_create
    drop_create()
    config = pconfig.set_trytond()
    return config


def drop_database():
    from trytond.tests.test_tryton import doctest_dropdb
    doctest_dropdb(None)


def connect_database(database, password='admin', database_type='postgresql'):
    return pconfig.set_trytond(database, password=password,
        config_file=os.environ.get('TRYTOND_CONFIG', 'trytond.conf'))