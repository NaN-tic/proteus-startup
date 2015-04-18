from proteus import Model, Wizard
from dateutil.relativedelta import relativedelta

AccountTemplate = Model.get('account.account.template')
Account = Model.get('account.account')
FiscalYear = Model.get('account.fiscalyear')
Sequence = Model.get('ir.sequence')
SequenceStrict = Model.get('ir.sequence.strict')
PaymentTerm = Model.get('account.invoice.payment_term')
PaymentTermLine = Model.get('account.invoice.payment_term.line')


def fiscal_year(date, company, post_move_seq):
    fiscal_year = FiscalYear(name=str(date.year))
    fiscal_year.start_date = date + relativedelta(month=1, day=1)
    fiscal_year.end_date = date + relativedelta(month=12, day=31)
    fiscal_year.company = company
    fiscal_year.post_move_sequence = post_move_seq
    return fiscal_year


def post_move_seq(name, company):
    return Sequence(name=name, code='account.move', company=company)


def invoice_seq(name, company):
    return SequenceStrict(name=name, code='account.invoice',
        company=company)


def account_expense(company):
    expense, = Account.find([
            ('kind', '=', 'expense'),
            ('company', '=', company.id),
            ])
    return expense


def account_revenue(company):
    revenue, = Account.find([
            ('kind', '=', 'revenue'),
            ('company', '=', company.id),
            ])
    return revenue


def account_receivable(company):
    receivable, = Account.find([
            ('kind', '=', 'receivable'),
            ('company', '=', company.id),
            ])
    return receivable


def account_payable(company):
    payable, = Account.find([
            ('kind', '=', 'payable'),
            ('company', '=', company.id),
            ])
    return payable


def payment_term_cash():
    payment_term = PaymentTerm(name='Cash Payment')
    payment_term_line = PaymentTermLine(type='remainder')
    payment_term.lines.append(payment_term_line)
    return payment_term


def chart_of_accounts(company):
    account_template, = AccountTemplate.find([('parent', '=', None)])
    create_chart = Wizard('account.create_chart')
    create_chart.execute('account')
    create_chart.form.account_template = account_template
    create_chart.form.company = company
    create_chart.execute('create_account')
    receivable, = Account.find([
            ('kind', '=', 'receivable'),
            ('company', '=', company.id),
            ])
    payable, = Account.find([
            ('kind', '=', 'payable'),
            ('company', '=', company.id),
            ])
    revenue, = Account.find([
            ('kind', '=', 'revenue'),
            ('company', '=', company.id),
            ])
    expense, = Account.find([
            ('kind', '=', 'expense'),
            ('company', '=', company.id),
            ])
    account_tax, = Account.find([
            ('kind', '=', 'other'),
            ('company', '=', company.id),
            ('name', '=', 'Main Tax'),
            ])
    create_chart.form.account_receivable = receivable
    create_chart.form.account_payable = payable
    return create_chart
