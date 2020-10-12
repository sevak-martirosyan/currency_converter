from rest_framework import serializers
from .models import Currency, Rate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('name', 'code')


class RateSerializer(serializers.ModelSerializer):
    currency_from = serializers.CharField(source='currency_from.code')
    currency_to = serializers.CharField(source='currency_to.code')

    class Meta:
        model = Rate
        fields = ('currency_from', 'currency_to', 'rate')
