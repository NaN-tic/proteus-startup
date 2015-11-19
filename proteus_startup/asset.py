# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model

from .common import create_model


__all__ = ['get_asset', 'create_asset']


def get_asset(type_, code=None, name=None):
    Asset = Model.get('asset')

    assert code or name, "Code ({}) or Name ({}) must be supplier".format(
        code, name)

    domain = [
        ('type', '=', type_),
        ]
    vals = {
        'type': type_,
        }
    if code:
        domain.append(('code', '=', code))
        vals['code'] = code
    if name:
        domain.append(('name', 'ilike', name))
        vals['name'] = name

    assets = Asset.find(domain)
    if assets:
        return assets[0]
    return create_asset(**vals)


@create_model('asset')
def create_asset(**kwargs):
    pass
