# Generated by Django 4.0.3 on 2022-06-29 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0006_alter_checkout_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='save_money',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
    ]