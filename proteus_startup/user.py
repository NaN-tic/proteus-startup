# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model

__all__ = ['reload_context']


def reload_context(config):
    User = Model.get('res.user')
    config._context = User.get_preferences(True, config.context)
