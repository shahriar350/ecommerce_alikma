from django.db import signals
from django.db.models.signals import pre_save
from django.dispatch import receiver

from EcommerceClient.mixins import unique_slug_generator
from basic_module_app.models import Category, Variation, Collection, Brand, ProductType
from product_app.models import Product


@receiver(pre_save, sender=Category)
def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.name = instance.name.lower()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=Variation)
def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.name = instance.name.lower()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=Collection)
def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.name = instance.name.lower()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=Brand)
def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.name = instance.name.lower()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=ProductType)
def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.name = instance.name.lower()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.name = instance.name.lower()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
