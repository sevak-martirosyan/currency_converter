from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/currencies/(?P<curr_from>[A-Z]{3})/(?P<curr_to>[A-Z]{3})',
         views.get_rate,
         name='get_rate'
         ),
    path('api/currencies/',
         views.get_currencies,
         name='get_currencies'
         )
]
