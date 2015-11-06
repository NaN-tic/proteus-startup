# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from proteus import Model, Wizard
from dateutil.relativedelta import relativedelta
from .common import create_model

__all__ = ['create_account_chart', 'create_fiscal_year',
    'get_post_move_sequence', 'get_invoice_sequence',
    'get_account_expense', 'get_account_revenue',
    'get_account_receivable', 'get_account_payable',
    'get_payment_term_cash', 'get_payment_type', 'similar_account',
    'get_code', 'get_similar_account']


def get_code(code, digits=7):
    if len(code) > 4:
        if code[:3] in ('430', '400', '410', '401', '440', '431'):
            return code[0:4].ljust(len(code), '0')
    return code


def get_similar_account(code, chart, digits=7):
    for digits in (digits, 4, 3, 2, 1):
        account = chart.get(get_similar_code(chart, code))
        if account:
            return account


def similar_account(sim_account, vals):
    Account = Model.get('account.account')
    account = Account()

    ignore_fields = ['id', 'code', 'name', 'childs', 'deferrals', 'taxes',
        'create_date', 'create_uid', 'write_date', 'write_uid', 'template',
        'parent']
    for field in Account._fields:
        if field in ignore_fields:
            continue
        value = getattr(sim_account, field)
        setattr(account, field, value)

    if (sim_account.code and sim_account.parent and
            len(vals.get('code', '')) == len(sim_account.code)):
        account.parent = sim_account.parent
    else:
        account.parent = sim_account

    for k, v in vals.iteritems():
        setattr(account, k, v)

    return account


def get_similar_code(chart, code, digits=7):
    l = len(code)
    if l > 4:
        code = code[0:4].ljust(digits, '0')
        if code in chart:
            return code

    for i in range(0, l):
        sub_code = code[:-i]
        if sub_code in chart:
            return sub_code


def get_chart_tree(company):
    Account = Model.get('account.account')
    accounts = Account.find([('company', '=', company)])
    return dict((a.code, a) for a in accounts)


@create_model('account.fiscalyear')
def create_fiscal_year(date, company, post_move_seq, invoice_sequence=None):
    values = {
        'name': str(date.year),
        'start_date': date + relativedelta(month=1, day=1),
        'end_date': date + relativedelta(month=12, day=31),
        'company': company,
        'post_move_sequence': post_move_seq,
    }
    if invoice_sequence is not None:
        values['out_invoice_sequence'] = invoice_sequence
        values['in_invoice_sequence'] = invoice_sequence
        values['out_credit_note_sequence'] = invoice_sequence
        values['in_credit_note_sequence'] = invoice_sequence
    return values


@create_model('ir.sequence')
def get_post_move_sequence(name, company):
    return {
        'name': name,
        'code': 'account.move',
        'company': company,
        }


@create_model('ir.sequence.strict')
def get_invoice_sequence(name, company):
    return {
        'name': name,
        'code': 'account.invoice',
        'company': company,
        }
    SequenceStrict = Model.get('ir.sequence.strict')
    return SequenceStrict(name=name, code='account.invoice',
        company=company)


def get_account_expense(company=None):
    return _get_account_by_type('expense', company=company)


def get_account_revenue(company=None):
    return _get_account_by_type('revenue', company=company)


def get_account_receivable(company=None):
    return _get_account_by_type('receivable', company=company)


def get_account_payable(company=None):
    return _get_account_by_type('payable', company=company)


def _get_account_by_type(type, company=None):
    Account = Model.get('account.account')
    domain = [
        ('kind', '=', type),
        ]
    if company:
        domain.append(('company', '=', company.id))
    accounts = Account.find(domain, limit=1)
    if accounts:
        return accounts[0]


def get_payment_type(name):
    PaymentType = Model.get('account.payment.type')
    existing = PaymentType.find([('name', '=', name)], limit=1)
    if existing:
        return existing[0]
    payment_type = PaymentType(name=name)
    payment_type.kind = 'receivable'
    return payment_type


def get_payment_term_cash(name='Cash Payment'):
    PaymentTerm = Model.get('account.invoice.payment_term')
    PaymentTermLine = Model.get('account.invoice.payment_term.line')

    existing = PaymentTerm.find([('name', '=', name)], limit=1)
    if existing:
        return existing[0]
    payment_term = PaymentTerm(name=name)
    payment_term_line = PaymentTermLine(type='remainder')
    payment_term.lines.append(payment_term_line)
    return payment_term


def create_account_chart(company, module=None, fs_id=None, digits=None):
    """
    Creates the chart of accounts defined by module and fs_id for the given
    company.

    If no 'module' and 'fs_id' are given, the last template chart created is
    used.
    """
    Account = Model.get('account.account')
    AccountTemplate = Model.get('account.account.template')
    ModelData = Model.get('ir.model.data')

    root_accounts = Account.find([('parent', '=', None)])
    if root_accounts:
        return

    if module and fs_id:
        data = ModelData.find([
                ('module', '=', module),
                ('fs_id', '=', fs_id),
                ], limit=1)

        assert len(data) == 1, ('Unexpected num of root templates '
            'with name "%s.%s": %s' % (module, fs_id, data))
        template = data[0].db_id
        template = AccountTemplate(template)
    else:
        template, = AccountTemplate.find([('parent', '=', None)],
            order=[('id', 'DESC')], limit=1)

    create_chart = Wizard('account.create_chart')
    create_chart.execute('account')
    create_chart.form.account_template = template
    create_chart.form.company = company
    if digits:
        create_chart.form.account_code_digits = int(digits)
    create_chart.execute('create_account')

    receivable, = Account.find([
            ('kind', '=', 'receivable'),
            ('company', '=', company.id),
            ], limit=1)
    payable, = Account.find([
            ('kind', '=', 'payable'),
            ('company', '=', company.id),
            ], limit=1)
    create_chart.form.account_receivable = receivable
    create_chart.form.account_payable = payable
    create_chart.execute('create_properties')
