# Generated by Django 2.1.3 on 2018-12-16 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='finaltotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=30),
        ),
    ]
