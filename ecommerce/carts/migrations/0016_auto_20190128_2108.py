# Generated by Django 2.1.3 on 2019-01-28 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0015_auto_20190128_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]