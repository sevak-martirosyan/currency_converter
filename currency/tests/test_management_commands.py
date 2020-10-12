from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from unittest.mock import patch, Mock
from ..models import Currency, Rate
from currency.management.commands import update_rates


class UpdateRatesTest(TestCase):
    def setUp(self):
        usd = Currency.objects.create(name='US Dollar', code='USD')
        Rate.objects.create(currency_from=usd, currency_to=usd, rate=1)

    def test_run_command(self):
        with patch('currency.management.commands.update_rates.requests.get') as mock_get:
            mock_get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"rates": {"USD": 1, "CZK": 1, "EUR": 1, "PLN": 1}}
            out = StringIO()
            call_command('update_rates', stdout=out)
            self.assertIn('All rates were fetched and saved successfully.', out.getvalue())

    def test_run_command_connection_error(self):
        with patch('currency.management.commands.update_rates.time') as mock_time:
            with patch('currency.management.commands.update_rates.requests.get',
                       side_effect=update_rates.requests.ConnectionError()) as mock_get:
                mock_time.sleep = Mock(return_value=None)
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"rates": {"USD": 1, "CZK": 1, "EUR": 1, "PLN": 1}}
                mock_get.return_value = mock_response
                out = StringIO()
                call_command('update_rates', stdout=out)
                self.assertIn('Could not connect to the service.', out.getvalue())

    def test_run_command_timeout_error(self):
        with patch('currency.management.commands.update_rates.time') as mock_time:
            with patch('currency.management.commands.update_rates.requests.get',
                       side_effect=update_rates.requests.Timeout()) as mock_get:
                mock_time.sleep = Mock(return_value=None)
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"rates": {"USD": 1, "CZK": 1, "EUR": 1, "PLN": 1}}
                mock_get.return_value = mock_response
                out = StringIO()
                call_command('update_rates', stdout=out)
                self.assertIn('Connection to the service timed out.', out.getvalue())