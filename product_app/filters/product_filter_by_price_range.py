import json
from decimal import Decimal

import django_filters
from django.core.exceptions import BadRequest
from django.db.models import Q, Prefetch

from basic_module_app.models import Category, Collection
from product_app.models import Product, ProductImage


def Convert(string):
    li = list(string.split("-"))
    return li


class ProductPriceRangeFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(label="Price", method='filter_show_min_price')

    class Meta:
        model = Product
        fields = ['brand',
                  'type',
                  'price']

    def filter_show_min_price(self, queryset, name, value):

        ids = []
        for i in queryset:
            if Decimal(self.data['price_min']) <= i.show_min_price <= Decimal(self.data['price_max']):
                ids.append(i.id)
        products = Product.objects.prefetch_related(
            Prefetch("get_product_images", queryset=ProductImage.objects.filter(primary=True).all())).filter(
            active=True, pk__in=ids)
        return products
