import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, object_records):
        self.records.append(object_records)

    def get_today_stats(self):
        sum_today = 0
        for date in self.records:
            if date.date == dt.datetime.now().date():
                sum_today += date.amount
        return sum_today

    def get_week_stats(self):
        sum_week = 0
        date_today = dt.date.today()
        week = date_today - dt.timedelta(days=7)
        for date in self.records:
            if week <= date.date <= date_today:
                sum_week += date.amount
        return sum_week


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        if date == '':
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CashCalculator(Calculator):
    USD_RATE = 7.55
    EURO_RATE = 91.74
    RUB_RATE = 1.0

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency_code):
        currencies_code = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE)
        }

        limit_remains = self.limit - self.get_today_stats()
        currency_code_name = currencies_code[currency_code][0]
        currency_code_rate = currencies_code[currency_code][1]
        remains_cash = round(limit_remains / currency_code_rate, 2)

        if remains_cash > 0:
            return f'На сегодня осталось {remains_cash} {currency_code_name}'
        elif remains_cash == 0:
            return f'Денег нет, держись'
        else:
            return (
                f'Денег нет, держись: твой долг - {abs(remains_cash)} '
                f'{currency_code_name}'
                )

        if currency_code not in currencies_code:
            return 'Направильно указана валюта! Попробуйте еще раз.'


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        used_today = self.get_today_stats()
        limit_remains = self.limit - used_today
        if limit_remains > 0:
            return (
                f'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {limit_remains} кКал'
                )
        elif limit_remains <= 0:
            return f'Хватит есть!'
