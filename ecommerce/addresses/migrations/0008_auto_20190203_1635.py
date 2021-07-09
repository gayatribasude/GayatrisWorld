# Generated by Django 2.1.3 on 2019-02-03 11:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0007_auto_20190127_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_line',
            field=models.TextField(default='BK 703/32, Mahalaxmi Nagar,Mumbai', verbose_name='Address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='contact_no',
            field=models.PositiveIntegerField(default=9130899803, max_length=10, validators=[django.core.validators.MinLengthValidator(10)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='full_name',
            field=models.CharField(default='Shraddha Vishwakarma', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.PositiveSmallIntegerField(default=1234567, max_length=7, validators=[django.core.validators.MinLengthValidator(7)]),
            preserve_default=False,
        ),
    ]