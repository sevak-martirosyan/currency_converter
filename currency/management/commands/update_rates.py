import requests
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from currency.models import Currency, Rate
from decimal import Decimal
import itertools


class Command(BaseCommand):
    help = 'Connects to openexchangerates.org, fetches the latest conversion rates, ' \
           'and updates the database with new rates.'
    currencies_to_get = ['USD', 'CZK', 'EUR', 'PLN']
    curr_names_dict = {
        'USD': 'US Dollar',
        'CZK': 'Czech Koruna',
        'EUR': 'Euro',
        'PLN': 'Zloty'
    }
    openexchangerates_url = 'https://openexchangerates.org/api/latest.json?app_id={}'

    def handle(self, *args, **options):
        """
        This function is run when manage.py update_rates command is issued
        Will connect to openexchangerates.org and fetch the latest exchange rates
        Edit the attributes above to change which currencies you want to have in your database
        """
        fetched_successfully = False
        retries = 0
        curr_model_objects = {}
        for currency in self.currencies_to_get:
            curr_obj, created = Currency.objects.get_or_create(code=currency, name=self.curr_names_dict[currency])
            curr_model_objects[currency] = curr_obj

        while not fetched_successfully:
            try:
                response_json = requests.get(self.openexchangerates_url.format(settings.OPENEXCHANGERATES_APP_ID))
                if response_json.status_code == 200:
                    fetched_successfully = True
                    # Calculating the rates for each possible pair of currencies given in self.currencies_to_get
                    for currency_pair in [p for p in itertools.product(self.currencies_to_get, repeat=2)]:
                        try:
                            rate = Rate.objects.get(currency_from=curr_model_objects[currency_pair[0]],
                                                    currency_to=curr_model_objects[currency_pair[1]])
                            rate.rate = Decimal(response_json.json()['rates'][currency_pair[1]]) / Decimal(
                                response_json.json()['rates'][currency_pair[0]])
                            rate.save()
                        except Rate.DoesNotExist:
                            rate = Rate(currency_from=curr_model_objects[currency_pair[0]],
                                        currency_to=curr_model_objects[currency_pair[1]],
                                        rate=Decimal(response_json.json()['rates'][currency_pair[1]]) / Decimal(
                                            response_json.json()['rates'][currency_pair[0]]))
                            rate.save()
            except requests.ConnectionError:
                self.stdout.write(self.style.ERROR('Could not connect to the service.'))
            except requests.Timeout:
                self.stdout.write(self.style.ERROR('Connection to the service timed out.'))
            # in case of connection problems, we will retry to get the rates 10 times,
            # with 10 minute wait time in between each request
            retries += 1
            if retries == 10:
                break

            if fetched_successfully:
                self.stdout.write(self.style.SUCCESS('All rates were fetched and saved successfully.'))
            else:
                time.sleep(600)
