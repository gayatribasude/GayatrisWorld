# Generated by Django 2.1.3 on 2019-01-31 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_conatct'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Conatct',
            new_name='Contact',
        ),
    ]