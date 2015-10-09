# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model

__all__ = ['get_group_by_xml_id']


def get_group_by_xml_id(module, fs_id):
    ModelData = Model.get('ir.model.data')
    Group = Model.get('res.group')

    data = ModelData.find([
            ('module', '=', module),
            ('fs_id', '=', fs_id),
            ], limit=1)
    if data:
        group_id = data[0].db_id
        return Group(group_id)
