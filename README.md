Simple web-based REST application for currency conversion. 
You will need an account on http://openexchangerates.org in order to be able to get the latest exchange rates.
Put APP ID from openexchangerates.org in OPENEXCHANGERATES_APP_ID in the settings.py file.

### Install and run.
This application requires Django 3.1.2 and Django REST Framework.
1. $ pip install -r requirements.txt
2. $ python3 manage.py migrate
3. $ python3 manage.py update_rates
4. $ python3 manage.py runserver 127.0.0.1:8000

Use crontab to update currency rates periodically.
Example: Update the rates every day at 10:00 AM .
1. $ crontab -e
2. Add to the file: [ 1 0 * * * python3 manage.py update_rates >/dev/null 2>&1 ] (without square brackets)

### Drive tests
1. $ python3 manage.py test