# Generated by Django 4.0.3 on 2022-06-01 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0004_alter_productvariation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]