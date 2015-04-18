from proteus import Model
from decimal import Decimal
import datetime
from dateutil.relativedelta import relativedelta


Currency = Model.get('currency.currency')
CurrencyRate = Model.get('currency.currency.rate')
today = datetime.datetime.combine(datetime.date.today(),
    datetime.datetime.min.time())


def get_currency(code):
    currencies = Currency.find([('code', '=', code)])

    if currencies:
        currency, = currencies
        return currency
    return None


def dollar():

    currency = get_currency('USD')

    if not currency:
        currency = Currency(name='US Dollar', symbol=u'$', code='USD',
            rounding=Decimal('0.01'), mon_grouping='[]',
            mon_decimal_point='.')

    currency_rate = CurrencyRate(date=today + relativedelta(month=1, day=1),
        rate=Decimal('1.0'), currency=currency)

    return currency, currency_rate


def euro():
    currency = get_currency('EUR')

    if not currency:
        currency = Currency(name='Euro', symbol=u'$', code='EUR',
            rounding=Decimal('0.01'), mon_grouping='[]',
            mon_decimal_point='.')
    currency_rate = CurrencyRate(date=today + relativedelta(month=1, day=1),
        rate=Decimal('1.0'), currency=currency)

    return currency, currency_rate
