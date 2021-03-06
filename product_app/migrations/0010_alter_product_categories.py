# Generated by Django 4.0.3 on 2022-07-02 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_module_app', '0014_alter_banner_image_alter_category_image_and_more'),
        ('product_app', '0009_alter_product_collections'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='get_category_products', to='basic_module_app.category'),
        ),
    ]
