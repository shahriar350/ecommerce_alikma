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
    categories = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), method='filter_category')
    collections = django_filters.ModelMultipleChoiceFilter(queryset=Collection.objects.all(),
                                                           method='filter_collections')

    def filter_category(self, queryset, name, value):
        print(self.data)
        if 'categories' in self.data and len(self.data.get('categories')) > 0:
            return queryset.filter(categories__in=self.data.get('categories'))
        else:
            return queryset

    def filter_collections(self, queryset, name, value):
        print(self.data)
        if 'collections' in self.data and len(self.data.get('collections')) > 0:
            return queryset.filter(collections__in=self.data.get('collections'))
        else:
            return queryset

    class Meta:
        model = Product
        fields = ['brand',
                  'type',
                  'categories',
                  'collections', 'price']

    def filter_show_min_price(self, queryset, name, value):

        ids = []
        for i in queryset:
            if Decimal(self.data['price_min']) <= i.show_min_price <= Decimal(self.data['price_max']):
                ids.append(i.id)
        products = Product.objects.prefetch_related(
            Prefetch("get_product_images", queryset=ProductImage.objects.filter(primary=True).all())).filter(
            active=True, pk__in=ids)
        return products
