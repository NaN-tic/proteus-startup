# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import os
from proteus import config as pconfig

__all__ = ['init_database', 'drop_database']


def init_database():

    from trytond.tests.test_tryton import drop_create
    drop_create()
    config = pconfig.set_trytond()
    return config


def drop_database(config):
    from trytond.tests.test_tryton import doctest_dropdb
    doctest_dropdb(None)
