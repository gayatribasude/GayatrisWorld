# Generated by Django 2.1.3 on 2019-01-27 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_remove_address_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='address',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='address',
            name='city',
        ),
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
        migrations.RemoveField(
            model_name='address',
            name='state',
        ),
        migrations.AddField(
            model_name='address',
            name='address_line',
            field=models.TextField(default='Hospital Area,BK-703/31 Ulhasnagar', verbose_name='Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='full_name',
            field=models.CharField(default='Gayatri Basude', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.PositiveSmallIntegerField(max_length=7),
        ),
    ]