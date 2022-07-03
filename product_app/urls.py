from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'main'
router = DefaultRouter()
# router.register("list", views.ProductList, basename="product-list")
router.register("basic/crud", views.ProductBasicCRUD, basename="product-basic-crud")
router.register("basic/operation", views.ProductOperation, basename="product-basic-operation")
router.register("variation/crud", views.ProductVariationCRUD, basename="product-variation-crud")
urlpatterns = [
    path("list/", views.ProductList.as_view(), name='product.list'),
    path("list/full/", views.ProductFullList.as_view(), name='product.list.full'),
    path("search/", views.UserSearchListView.as_view(), name='product.list.search.name'),
    path("filter/brand/<int:id>/", views.ProductFilterByBrand.as_view(), name='product.list.filter.brand'),
    path("filter/category/<int:id>/", views.ProductFilterByCategory.as_view(), name='product.list.filter.category'),
    path("filter/collection/<int:id>/", views.ProductFilterByCollections.as_view(), name='product.list.filter'
                                                                                         '.collection'),
    path("filter/type/<int:id>/", views.ProductFilterByType.as_view(), name='product.list.filter.type'),
    path("filter/type/<int:id>/", views.ProductFilterByType.as_view(), name='product.list.filter.type'),
    path("top_selling/", views.TopSellingProduct.as_view(), name='product.top.selling'),


]
urlpatterns += router.urls
