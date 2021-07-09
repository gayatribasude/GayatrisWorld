# Generated by Django 2.1.3 on 2019-01-29 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0020_auto_20190129_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='cart_in_item',
        ),
        migrations.RemoveField(
            model_name='item',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='item_in_cart',
        ),
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, to='products.Product'),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]