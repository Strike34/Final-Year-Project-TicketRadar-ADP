# Generated by Django 4.0 on 2024-03-06 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_account_address_remove_account_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='amount',
            field=models.IntegerField(default=1000),
        ),
    ]
