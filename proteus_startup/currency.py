# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from proteus import Model
import datetime

__all__ = ['get_currency', 'get_dollar', 'get_euro']

today = datetime.datetime.combine(datetime.date.today(),
    datetime.datetime.min.time())


def get_currency(config, code):
    Currency = Model.get('currency.currency')
    currencies = Currency.find([('code', '=', code)])

    if currencies:
        currency, = currencies
        return currency
    return None


def get_dollar(config):
    Currency = Model.get('currency.currency')
    CurrencyRate = Model.get('currency.currency.rate')

    currency = get_currency(config, 'USD')

    if not currency:
        currency = Currency(name='US Dollar', symbol=u'$', code='USD',
            rounding=Decimal('0.01'), mon_grouping='[]',
            mon_decimal_point='.')

    if not currency.rates:
        currency.rates.append(
            CurrencyRate(
                date=today + relativedelta(month=1, day=1),
                rate=Decimal('1.0')))

    return currency


def get_euro(config):
    Currency = Model.get('currency.currency')
    CurrencyRate = Model.get('currency.currency.rate')

    currency = get_currency(config, 'EUR')

    if not currency:
        currency = Currency(name='Euro', symbol=u'$', code='EUR',
            rounding=Decimal('0.01'), mon_grouping='[]',
            mon_decimal_point='.')

    if not currency.rates:
        currency.rates.append(
            CurrencyRate(
                date=today + relativedelta(month=1, day=1),
                rate=Decimal('1.0')))

    return currency
