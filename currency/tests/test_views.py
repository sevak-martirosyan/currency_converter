from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Currency, Rate
from ..serializers import CurrencySerializer, RateSerializer


client = Client()


class GetCurrenciesTest(TestCase):

    def setUp(self):
        Currency.objects.create(name='US Dollar', code='USD')
        Currency.objects.create(name='Czech Koruna', code='CZK')
        Currency.objects.create(name='Euro', code='EUR')
        Currency.objects.create(name='Zloty', code='PLN')

    def test_get_currencies(self):
        response = client.get(reverse('get_currencies'))

        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetRateTest(TestCase):

    def setUp(self):
        self.usd = Currency(name='US Dollar', code='USD')
        self.koruna = Currency(name='Czech Koruna', code='CZK')
        self.euro = Currency(name='Euro', code='EUR')
        self.zloty = Currency(name='Zloty', code='PLN')

        self.usd.save()
        self.koruna.save()
        self.euro.save()
        self.zloty.save()

        Rate.objects.create(currency_from=self.usd, currency_to=self.koruna, rate=20.696238)
        Rate.objects.create(currency_from=self.usd, currency_to=self.euro, rate=0.814052)
        Rate.objects.create(currency_from=self.usd, currency_to=self.zloty, rate=3.433291)
        Rate.objects.create(currency_from=self.usd, currency_to=self.usd, rate=1)

    def test_get_rate(self):
        response = client.get(reverse('get_rate', kwargs={"curr_from": "USD", "curr_to": "EUR"}))
        rate = Rate.objects.get(currency_from=self.usd, currency_to=self.euro)
        serializer = RateSerializer(rate)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rate_missing_rate(self):
        rate = Rate.objects.get(currency_from=self.usd, currency_to=self.euro)
        rate.delete()
        response = client.get(reverse('get_rate', kwargs={"curr_from": "USD", "curr_to": "EUR"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_rate_missing_currency(self):
        self.usd.delete()
        response = client.get(reverse('get_rate', kwargs={"curr_from": "USD", "curr_to": "EUR"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
