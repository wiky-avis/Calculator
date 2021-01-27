import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, object_records):
        self.records.append(object_records)

    def get_today_stats(self):
        return sum(
            date.amount for date in self.records 
            if date.date == dt.date.today()
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
        if date:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()


class CashCalculator(Calculator):
    USD_RATE = 7.55
    EURO_RATE = 91.74
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency_code):
        currencies_code = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE)
        }

        limit_remains = self.limit - self.get_today_stats()
        currency_code_name, currency_code_rate = currencies_code[currency_code]
        remains_cash = round(limit_remains / currency_code_rate, 2)

        if remains_cash > 0:
            return f'На сегодня осталось {remains_cash} {currency_code_name}'
        elif remains_cash == 0:
            return 'Денег нет, держись'
        else:
            remains_cash = abs(remains_cash)
            return (
                f'Денег нет, держись: твой долг - {remains_cash} '
                f'{currency_code_name}'
                )

        if currency_code not in currencies_code:
            return 'Направильно указана валюта! Попробуйте еще раз.'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        used_today = self.get_today_stats()
        limit_remains = self.limit - used_today
        if limit_remains > 0:
            return (
                f'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {limit_remains} кКал'
                )
        return 'Хватит есть!'



cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=145, comment="кофе")) 
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", \
    date="11.11.2020"))
                
print(cash_calculator.get_today_cash_remained("rub"))
print(cash_calculator.get_today_cash_remained("usd"))
print(cash_calculator.get_today_cash_remained("eur"))

calories_calculator = CaloriesCalculator(1500)
calories_calculator.add_record(Record(amount=1186, comment="Кусок тортика. \
    И ещё один."))
calories_calculator.add_record(Record(amount=84, comment="Йогурт."))
calories_calculator.add_record(Record(amount=1140, comment="Баночка чипсов.",\
    date="24.02.2019"))
calories_calculator.add_record(Record(amount=145, comment="кофе"))
calories_calculator.add_record(Record(amount=145, comment="кофе"))

print(calories_calculator.get_calories_remained())
print(calories_calculator.get_week_stats(), 'кКал')