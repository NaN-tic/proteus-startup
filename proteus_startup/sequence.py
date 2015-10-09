# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model

__all__ = ['get_sequence']


def get_sequence(strict, code, name, prefix=None, suffix=None,
        sequence_type=None, number_increment=None, padding=None, company=None):
    if strict:
        Sequence = Model.get('ir.sequence.strict')
    else:
        Sequence = Model.get('ir.sequence')

    domain = [
        ('code', '=', code),
        ]
    if name:
        domain.append(('name', '=', name))
    if company:
        domain.append(('company', '=', company.id))

    sequences = Sequence.find(domain)
    if sequences:
        return sequences[0]

    return create_sequence(strict, code, name, prefix=prefix, suffix=suffix,
        sequence_type=sequence_type, number_increment=number_increment,
        padding=padding)


def create_sequence(strict, code, name, prefix=None, suffix=None,
        sequence_type=None, number_increment=None, padding=None, company=None):
    if strict:
        Sequence = Model.get('ir.sequence.strict')
    else:
        Sequence = Model.get('ir.sequence')

    sequence = Sequence()
    sequence.name = name
    sequence.code = code
    if prefix:
        sequence.prefix = prefix
    if suffix:
        sequence.suffix = suffix
    if sequence_type:
        sequence.type = sequence_type
    if number_increment:
        sequence.number_increment = number_increment
    if padding:
        sequence.padding = padding
    if company:
        sequence.company = company
    return sequence
