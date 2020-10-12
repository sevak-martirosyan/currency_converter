from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=6, max_digits=20)),
                ('currency_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency_from', to='currency.Currency')),
                ('currency_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency_to', to='currency.Currency')),
            ],
        ),
    ]