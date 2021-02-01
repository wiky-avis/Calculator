import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, object_records):
        self.records.append(object_records)

    def get_today_stats(self):
        date_today = dt.date.today()
        return sum(
            date.amount for date in self.records
            if date.date == date_today
            )

    def get_week_stats(self):
        date_today = dt.date.today()
        week = date_today - dt.timedelta(days=7)
        return sum(
            date.amount for date in self.records
            if week <= date.date <= date_today
            )


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CashCalculator(Calculator):
    USD_RATE = 75.55
    EURO_RATE = 91.74
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency_code):
        limit_remains = self.limit - self.get_today_stats()

        if limit_remains == 0:
            return 'Денег нет, держись'

        currencies_code = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE)
        }

        if currency_code not in currencies_code:
            raise ValueError(
                'Направильно указана валюта! Попробуйте еще раз.'
                )

        currency_code_name, currency_code_rate = currencies_code[currency_code]
        remains_cash = round(limit_remains / currency_code_rate, 2)

        if limit_remains > 0:
            return f'На сегодня осталось {remains_cash} {currency_code_name}'
        else:
            remains_cash = abs(remains_cash)
            return (
                f'Денег нет, держись: твой долг - {remains_cash} '
                f'{currency_code_name}'
                )


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        used_today = self.get_today_stats()
        limit_remains = self.limit - used_today
        if limit_remains > 0:
            return (
                'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {limit_remains} кКал'
                )
        return 'Хватит есть!'
