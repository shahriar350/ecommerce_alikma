import datetime
import os
from decimal import Decimal
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from datetime import datetime

from django.db.models import Min, Max
from django.utils import timezone
from django_quill.fields import QuillField

from EcommerceClient.mixins import CUMixin
from basic_module_app.models import Brand, Category, Collection, ProductType, Variation

User = get_user_model()


def path_and_rename(instance, filename):
    upload_to = 'products'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Product(CUMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(editable=False)
    sku = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    product_price = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    selling_price = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    offer_price = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    offer_start = models.DateTimeField(null=True, blank=True)
    offer_end = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    next_stock_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="get_brand_products")
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="get_type_products")
    categories = models.ManyToManyField(Category, related_name="get_category_products", blank=True)
    collections = models.ManyToManyField(Collection, related_name="get_collection_products", blank=True)

    @property
    def is_offer_valid(self):
        if self.offer_start is not None and self.offer_end is not None:
            return self.offer_start <= timezone.now() <= self.offer_end
        else:
            return False

    @property
    def final_price(self) -> Decimal:
        if self.is_offer_valid:
            return self.selling_price - self.offer_price
        else:
            return self.selling_price

    @property
    def first_page_showing_price(self) -> str:
        if not self.get_product_variations.exists():
            if self.is_offer_valid:
                return '৳' + str(self.selling_price - self.offer_price)
            else:
                return '৳' + str(self.selling_price)
        else:
            all_variation = self.get_product_variations.all()
            minprice = all_variation.aggregate(Min('selling_price'))
            maxprice = all_variation.aggregate(Max('selling_price'))
            print(minprice, maxprice)
            if minprice['selling_price__min'] == maxprice['selling_price__max']:
                if self.is_offer_valid:
                    return '৳' + str(Decimal(minprice['selling_price__min']) - self.offer_price)
                else:
                    return '৳' + str(minprice['selling_price__min'])
            else:
                if self.is_offer_valid:
                    return '৳' + str(Decimal(minprice['selling_price__min']) - self.offer_price) + ' - ' + '৳' + \
                           str(Decimal(maxprice['selling_price__max']) - self.offer_price)
                else:
                    return '৳' + str(minprice['selling_price__min']) + ' - ' + '৳' + str(maxprice['selling_price__max'])

    @property
    def show_min_price(self) -> Decimal:
        if not self.get_product_variations.exists():
            if self.is_offer_valid:
                return self.selling_price - self.offer_price
            else:
                return self.selling_price
        else:
            all_variation = self.get_product_variations.all()
            minprice = all_variation.aggregate(Min('selling_price'))
            if self.is_offer_valid:
                return minprice['selling_price__min'] - self.offer_price
            else:
                return minprice['selling_price__min']

    def __str__(self):
        return self.name


class ProductImage(CUMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="get_product_images")
    image = models.ImageField(upload_to=path_and_rename,max_length=500)
    primary = models.BooleanField(default=False)


class ProductVariation(CUMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="get_product_variations")
    sku = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    product_price = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    selling_price = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to=path_and_rename)

    @property
    def final_price(self):
        if self.product.is_offer_valid:
            print(f'offer price is {self.selling_price - self.product.offer_price}')
            return self.selling_price - self.product.offer_price
        else:
            print(f'not offer price is {self.selling_price}')
            return self.selling_price


class ProductVariationValues(CUMixin):
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE,
                                          related_name="get_product_variation_values")
    variation = models.ForeignKey(Variation, on_delete=models.SET_NULL, related_name="get_variation_product_values",
                                  null=True, blank=True)
    title = models.CharField(max_length=255)


class ProductRequest(CUMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="get_product_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="get_user_requests")
    quantity = models.PositiveIntegerField(default=0)
