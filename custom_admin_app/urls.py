from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'main'

urlpatterns = [
    path('dashboard/', views.IndexPage.as_view(), name='dashboard'),
    path('basic/category/', views.CategoryIndex.as_view(), name='category.index'),
    path('basic/category/create/', views.CategoryCreate.as_view(), name='category.create'),
    path('basic/category/edit/<int:pk>/', views.CategoryUpdate.as_view(), name='category.update'),
    path('basic/category/delete/<int:pk>/', views.CategoryDelete.as_view(), name='category.delete'),
    # variation
    path('basic/variation/', views.VariationIndex.as_view(), name='variation.index'),
    path('basic/variation/create/', views.VariationCreate.as_view(), name='variation.create'),
    path('basic/variation/edit/<int:pk>/', views.VariationUpdate.as_view(), name='variation.update'),
    path('basic/variation/delete/<int:pk>/', views.VariationDelete.as_view(), name='variation.delete'),
    # variation
    path('basic/collection/', views.CollectionIndex.as_view(), name='collection.index'),
    path('basic/collection/create/', views.CollectionCreate.as_view(), name='collection.create'),
    path('basic/collection/edit/<int:pk>/', views.CollectionUpdate.as_view(), name='collection.update'),
    path('basic/collection/delete/<int:pk>/', views.CollectionDelete.as_view(), name='collection.delete'),
    # brand
    path('basic/brand/', views.BrandIndex.as_view(), name='brand.index'),
    path('basic/brand/create/', views.BrandCreate.as_view(), name='brand.create'),
    path('basic/brand/edit/<int:pk>/', views.BrandUpdate.as_view(), name='brand.update'),
    path('basic/brand/delete/<int:pk>/', views.BrandDelete.as_view(), name='brand.delete'),
    # product type
    path('basic/type/', views.TypeIndex.as_view(), name='type.index'),
    path('basic/type/create/', views.TypeCreate.as_view(), name='type.create'),
    path('basic/type/edit/<int:pk>/', views.TypeUpdate.as_view(), name='type.update'),
    path('basic/type/delete/<int:pk>/', views.TypeDelete.as_view(), name='type.delete'),
    # coupon type
    path('basic/coupon/', views.CouponIndex.as_view(), name='coupon.index'),
    path('basic/coupon/create/', views.CouponCreate.as_view(), name='coupon.create'),
    path('basic/coupon/edit/<int:pk>/', views.CouponUpdate.as_view(), name='coupon.update'),
    path('basic/coupon/delete/<int:pk>/', views.CouponDelete.as_view(), name='coupon.delete'),
    # product
    path('product/', views.ProductIndex.as_view(), name='product.index'),
    path('product/create/basic/', views.ProductCreate.as_view(), name='product.create.basic'),
    path('product/create/variance/<int:pk>/', views.ProductVarianceCreate.as_view(), name='product.create.variance'),
    path('product/save/variance/', views.ProductVarianceCreateSave.as_view(), name='product.create.variance.save'),
    path('product/create/images/<int:pk>/', views.ProductImageCreate.as_view(), name='product.create.image'),

]
