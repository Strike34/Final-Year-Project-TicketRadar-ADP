# Generated by Django 4.0 on 2024-03-05 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_account_address_remove_account_phone_and_more'),
        ('event', '0007_remove_ticket_ticket_holder_ticket_ticket_holder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_holder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_ticket', to='account.account'),
        ),
    ]
