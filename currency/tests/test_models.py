from django.test import TestCase
from ..models import Currency, Rate


class CurrencyTest(TestCase):

    def setUp(self):
        Currency.objects.create(name='US Dollar', code='USD')
        Currency.objects.create(name='Czech Koruna', code='CZK')
        Currency.objects.create(name='Euro', code='EUR')
        Currency.objects.create(name='Zloty', code='PLN')

    def test_get_currency_name_code(self):
        usd = Currency.objects.get(code='USD')
        euro = Currency.objects.get(code='EUR')
        koruna = Currency.objects.get(code='CZK')
        zloty = Currency.objects.get(code='PLN')

        self.assertEqual(usd.get_currency_name_code(), "The code for currency name US Dollar is USD.")
        self.assertEqual(euro.get_currency_name_code(), "The code for currency name Euro is EUR.")
        self.assertEqual(koruna.get_currency_name_code(), "The code for currency name Czech Koruna is CZK.")
        self.assertEqual(zloty.get_currency_name_code(), "The code for currency name Zloty is PLN.")


class RateTest(TestCase):

    def setUp(self):
        usd = Currency(name='US Dollar', code='USD')
        koruna = Currency(name='Czech Koruna', code='CZK')
        euro = Currency(name='Euro', code='EUR')
        zloty = Currency(name='Zloty', code='PLN')

        usd.save()
        koruna.save()
        euro.save()
        zloty.save()

        Rate.objects.create(currency_from=usd, currency_to=koruna, rate=20.696238)
        Rate.objects.create(currency_from=usd, currency_to=euro, rate=0.814052)
        Rate.objects.create(currency_from=usd, currency_to=zloty, rate=3.433291)
        Rate.objects.create(currency_from=usd, currency_to=usd, rate=1)

    def test_get_conversion_rate(self):
        usd = Currency.objects.get(code='USD')
        euro = Currency.objects.get(code='EUR')
        koruna = Currency.objects.get(code='CZK')
        zloty = Currency.objects.get(code='PLN')

        usd_to_koruna = Rate.objects.get(currency_from=usd, currency_to=koruna)
        usd_to_euro = Rate.objects.get(currency_from=usd, currency_to=euro)
        usd_to_zloty = Rate.objects.get(currency_from=usd, currency_to=zloty)
        usd_to_usd = Rate.objects.get(currency_from=usd, currency_to=usd)

        self.assertEqual(usd_to_koruna.get_conversion_rate(), "1 USD is equal to 20.696238 CZK.")
        self.assertEqual(usd_to_euro.get_conversion_rate(), "1 USD is equal to 0.814052 EUR.")
        self.assertEqual(usd_to_zloty.get_conversion_rate(), "1 USD is equal to 3.433291 PLN.")
        self.assertEqual(usd_to_usd.get_conversion_rate(), "1 USD is equal to 1.000000 USD.")