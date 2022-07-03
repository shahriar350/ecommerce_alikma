from django.contrib import admin

# Register your models here.
from django.template.response import TemplateResponse
from django.urls import path
from mptt.admin import DraggableMPTTAdmin

from basic_module_app.models import Category, Variation, Collection, Brand, ProductType, \
    UserAddress, District, Division, DeliveryFreeArea


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_filter = ['id', 'name']


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    model = Variation
    list_display = ['id', 'name']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    list_display = ['id', 'name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['id', 'name']


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    list_display = ['id', 'name']


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    model = Division
    list_display = ['id', 'name']


@admin.register(District)
class DivisionAdmin(admin.ModelAdmin):
    model = District
    list_display = ['id', 'name', 'division']
    sortable_by = ['division']


@admin.register(DeliveryFreeArea)
class DeliveryFreeAreaAdmin(admin.ModelAdmin):
    model = DeliveryFreeArea
    list_display = ['id', 'post_office']


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    model = UserAddress
    list_display = ['id', 'area',
                    'street',
                    'house',
                    'post_office',
                    'district',
                    'division', ]
