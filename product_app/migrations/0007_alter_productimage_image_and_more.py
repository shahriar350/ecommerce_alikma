# Generated by Django 4.0.3 on 2022-06-04 10:55

from django.db import migrations, models
import product_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0006_alter_productimage_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=product_app.models.path_and_rename),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=product_app.models.path_and_rename),
        ),
    ]
