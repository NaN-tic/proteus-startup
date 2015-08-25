# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model

__all__ = ['get_language']


def get_language(code):
    Lang = Model.get('ir.lang')

    if not code:
        return

    langs = Lang.find([('code', '=', code)])
    if langs:
        return langs[0]
