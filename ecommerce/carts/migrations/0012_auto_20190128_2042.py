# Generated by Django 2.1.3 on 2019-01-28 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0011_auto_20190128_2033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='products',
            new_name='product',
        ),
    ]
