# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from calendar import monthrange
from collections import OrderedDict
from datetime import date
from proteus import Model, Wizard
from dateutil.relativedelta import relativedelta
import datetime
from .common import create_model

__all__ = ['create_account_chart', 'create_fiscal_year',
    'get_post_move_sequence', 'get_invoice_sequence',
    'get_account_expense', 'get_account_revenue',
    'get_account_receivable', 'get_account_payable',
    'get_payment_term_cash', 'get_payment_type', 'similar_account',
    'get_code', 'get_similar_account', 'create_journal', 'create_move',
    'create_move_line']


def party_codes():
    return ('430', '400', '410', '401', '440', '431')


def get_code(code, digits=7):
    if len(code) > 4:
        if code[:3] in party_codes():
            return code[0:4].ljust(len(code), '0')
    return code


def get_similar_account(code, chart, digits=7):

    if len(code) < digits:
        for digits in (4, 3, 2, 1):
            code2 = code[:digits]
            account = chart.get(code2)
            if account:
                break

    if len(code) == digits:
        # Ensure that we find a valid account
        for i in range(len(code)):
            sub_code = code[:-i].ljust(digits, '0')
            if sub_code in chart:
                new_account = chart.get(sub_code)
                if new_account.kind != 'view':
                    account = new_account
                    break

    if account:
        return account


def similar_account(sim_account, vals):
    Account = Model.get('account.account')
    account = Account()

    ignore_fields = ['id', 'code', 'name', 'childs', 'deferrals', 'taxes',
        'create_date', 'create_uid', 'write_date', 'write_uid', 'template',
        'parent', 'company', 'general_ledger_balance', 'balance', 'credit',
        'debit', 'right', 'left']

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
    return dict((str(a.code), a) for a in accounts)


@create_model('account.fiscalyear')
def create_fiscal_year(year, company, post_move_seq, invoice_sequence=None):
    Fiscalyear = Model.get('account.fiscalyear')
    start_date = date(year=year, month=1, day=1)
    end_date = date(year=year, month=12, day=31)
    name = str(date.year)
    fiscalyears = Fiscalyear.find([
            ('name', '=', name),
            ('start_date', '=', start_date),
            ('end_date', '=', end_date),
            ('company', '=', company.id),
            ], limit=1)
    if fiscalyears:
        return fiscalyears[0]
    values = {
        'name': name,
        'company': company,
        'start_date': start_date,
        'end_date': end_date,
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


def get_payment_type(name, kind=None):
    PaymentType = Model.get('account.payment.type')
    domain = [('name', '=', name)]
    if kind:
        domain.append(('kind', '=', 'payable'))
    existing = PaymentType.find(domain, limit=1)
    if existing:
        return existing[0]
    payment_type = PaymentType(name=name)
    payment_type.kind = kind or 'receivable'
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


@create_model('account.journal')
def create_journal(**kwargs):
    Journal = Model.get('account.journal')
    domain = []
    if 'name' in kwargs:
        domain.append(('name', '=', kwargs.get('name')))
    if 'code' in kwargs:
        domain.append(('code', '=', kwargs.get('code')))
    if domain:
        journals = Journal.find(domain, limit=1)
        if journals:
            return journals[0]


@create_model('account.move')
def create_move(**kwargs):
    pass


@create_model('account.move.line')
def create_move_line(**kwargs):
    pass


class MonthlyPeriodGetter(OrderedDict):
    '''
    Returns the account period of a date.
    It asumes that Monthly periods are created, and it makes a cache of
    it to avoid reading values so much time.

    Usage:

        periods = MontlhlyPeriodGetter()
        p1 = periods.get(date(2015, 1, 1))  #It will fetch from db
        p2 = periods.get(date(2015, 1, 2))  #It will return from cache
    '''
    def __init__(self, *args, **kwargs):
        super(MonthlyPeriodGetter, self).__init__(*args, **kwargs)
        if kwargs.get('load', True):
            Period = Model.get('account.period')
            periods = Period.find([])
            for period in periods:
                key = (period.start_date.year, period.start_date.month)
                self.__setitem__(key, period)

    def __getitem__(self, key):
        if (isinstance(key, datetime.date) or
                isinstance(key, datetime.datetime)):
            key = (key.year, key.month)
        return super(MonthlyPeriodGetter, self).__getitem__(key)

    def __missing__(self, key):
        Period = Model.get('account.period')
        year, month = key
        _, last_day = monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, last_day)
        periods = Period.find([
                ('start_date', '=', start_date),
                ('end_date', '=', end_date),
                ], limit=1)
        if periods:
            period = periods[0]
            self.__setitem__(key, period)
            return period
        return super(MonthlyPeriodGetter, self).__missing__(key)
