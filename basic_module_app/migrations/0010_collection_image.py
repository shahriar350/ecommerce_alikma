# Generated by Django 4.0.5 on 2022-06-22 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_module_app', '0009_remove_usercoupon_payment_delete_couponbank'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
