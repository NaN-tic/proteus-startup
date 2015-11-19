# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model

from .common import create_model

__all__ = ['add_allowed_document', 'get_proof', 'get_method',
    'add_possible_values']


def add_allowed_document(company, model_name, quality_sequence=None):
    Configuration = Model.get('quality.configuration')
    IrModel = Model.get('ir.model')
    Sequence = Model.get('ir.sequence')

    configuration = Configuration(1)
    for allowed_document in configuration.allowed_documents:
        if (allowed_document.company == company
                and allowed_document.document.model == model_name):
            return

    model, = IrModel.find([('model', '=', model_name)])
    if not quality_sequence:
        quality_sequence = Sequence.find([('code', '=', 'quality.test')])[0]

    allowed_document = configuration.allowed_documents.new()
    allowed_document.company = company
    allowed_document.document = model
    allowed_document.quality_sequence = quality_sequence
    configuration.save()


@create_model('quality.proof')
def get_proof(name, type, company):
    Proof = Model.get('quality.proof')

    domain = [
        ('name', '=', name),
        ('type', '=', type),
        ]
    if company:
        domain.append(('company', '=', company.id))
    proofs = Proof.find(domain)
    if proofs:
        return proofs[0]

    return {
        'name': name,
        'type': type,
        'company': company,
        }


@create_model('quality.proof.method')
def get_method(name, proof):
    Method = Model.get('quality.proof.method')

    if proof.id > 0:
        methods = Method.find([
                ('proof', '=', proof.id),
                ('name', '=', name),
                ])
        if methods:
            return methods[0]
        return {
            'name': name,
            'proof': proof,
            }

    method = proof.methods.new()
    method.name = name
    return method


def add_possible_values(method, values):
    to_add = values[:]
    for value in method.possible_values:
        if value.name in to_add:
            to_add.remove(value.name)
    for v_name in to_add:
        qvalue = method.possible_values.new()
        qvalue.name = v_name
