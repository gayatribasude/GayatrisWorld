# Generated by Django 2.1.3 on 2019-01-30 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0025_auto_20190130_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
