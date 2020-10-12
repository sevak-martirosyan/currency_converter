from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique='True')
    name = models.CharField(max_length=30)

    def get_currency_name_code(self):
        return "The code for currency name {} is {}.".format(self.name, self.code)


class Rate(models.Model):
    currency_from = models.ForeignKey(Currency, related_name='currency_from', on_delete=models.CASCADE)
    currency_to = models.ForeignKey(Currency, related_name='currency_to', on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=20, decimal_places=6)

    def get_conversion_rate(self):
        return "1 {} is equal to {} {}.".format(self.currency_from.code, self.rate, self.currency_to.code)
