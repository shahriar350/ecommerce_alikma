from django.contrib import admin

# Register your models here.
import nested_admin
from nested_admin.nested import NestedStackedInline, NestedModelAdmin

from product_app.models import Product, ProductImage, ProductVariation, ProductVariationValues


class ProductImagesAdmin(NestedStackedInline):
    model = ProductImage


class ProductVariationValuesAdmin(NestedStackedInline):
    model = ProductVariationValues
    extra = 1

class ProductVariationsAdmin(NestedStackedInline):
    model = ProductVariation
    inlines = [ProductVariationValuesAdmin]
    extra = 0


@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    model = Product
    inlines = [ProductImagesAdmin, ProductVariationsAdmin]
