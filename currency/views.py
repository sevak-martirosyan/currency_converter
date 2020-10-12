from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Currency, Rate
from .serializers import CurrencySerializer, RateSerializer


@api_view(['GET'])
def get_currencies(request):
    if request.method == 'GET':
        currencies = Currency.objects.all()
        serialized = CurrencySerializer(currencies, many=True)
        return Response(serialized.data)


@api_view(['GET'])
def get_rate(request, curr_from, curr_to):
    try:
        currency_from = Currency.objects.get(code=curr_from)
        currency_to = Currency.objects.get(code=curr_to)
        rate = Rate.objects.get(currency_from=currency_from, currency_to=currency_to)
    except Currency.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Rate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serialized = RateSerializer(rate)
        return Response(serialized.data)


def index(request):
    return render(request, 'index.html')