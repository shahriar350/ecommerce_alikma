# Generated by Django 4.0.5 on 2022-06-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_module_app', '0005_coupon_free_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercoupon',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]