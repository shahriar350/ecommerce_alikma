from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("category", views.CategoryView, basename='category')
router.register("variation", views.VariationView, basename='Variation')
router.register("collection", views.CollectionView, basename='Collection')
router.register("brand", views.BrandView, basename='Brand')

router.register("type", views.ProductTypeView, basename='ProductType')
router.register("user/address", views.UserAddressView, basename='UserAddress')

urlpatterns = [
    path('division/district/all/', views.DivisionAllView.as_view()),
    path('banner/', views.BannerList.as_view()),
    # path('coupon/buy/', views.CouponBuyView.as_view()),
    # path('coupon/payment/complete/', views.CouponPaymentCompleteView.as_view()),
    # path('coupon/payment/failed/', views.CouponPaymentFailedView.as_view()),
    # path('coupon/payment/cancel/', views.CouponPaymentCancelView.as_view()),
]
urlpatterns += router.urls
