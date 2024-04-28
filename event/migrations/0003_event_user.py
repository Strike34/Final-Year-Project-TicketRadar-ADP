# Generated by Django 4.0 on 2024-02-21 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_account_address_remove_account_phone_and_more'),
        ('event', '0002_alter_ticket_event_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.account'),
        ),
    ]