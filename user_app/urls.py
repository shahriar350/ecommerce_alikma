from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("address", views.UserAddressView, basename='UserUAddress')
urlpatterns = [
    path('add/product/to/cart/', views.CartProductView.as_view()),
    path('carts/', views.CartList.as_view()),
    path('cart/products/count/', views.CartProductCount.as_view()),
    path('cart/remove/product/<int:product_id>/', views.CartProductRemove.as_view()),
    path('checkout/', views.CartCheckout.as_view()),
    path('payment/success/', views.PaymentSuccessSSL.as_view()),
    path('payment/fail/', views.payment_fail_ssl),
    path('payment/cancel/', views.payment_cancel_ssl),
    path('payment/ipn/', views.payment_ipn_ssl),
    path('search/coupon/', views.SearchCouponView.as_view()),
    path('order/all/', views.OrderList.as_view()),
    path('basic/info/', views.UserInfoView.as_view()),
    path('password/reset/', views.UserPasswordReset.as_view()),
    path("order/history/", views.OrderHistoryView.as_view(), name='user.order.history'),
    path("order/track/<slug:order_id>/", views.OrderTrackView.as_view(), name='user.order.track'),

]
urlpatterns += router.urls
