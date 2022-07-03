from django.urls import path

from basic_module_app.views import DivisionAllView
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("basic/category", views.CategoryView, basename='category-admin')
router.register("basic/user", views.UserView, basename='user-info-admin')
router.register("basic/variation", views.VariationView, basename='variation-admin')
router.register("basic/collection", views.CollectionView, basename='collection-admin')
router.register("basic/brand", views.BrandView, basename='brand-admin')
router.register("basic/type", views.ProductTypeView, basename='productType-admin')
router.register("basic/coupon", views.CouponView, basename='coupon-admin')
router.register("basic/banner", views.BannerView, basename='banner-admin')
router.register("basic/user/address", views.UserAddressView, basename='userAddress-admin')
router.register("division", views.DivisionView, basename="district-admin")
router.register("district", views.DistrictView, basename="district-admin")
router.register("post_office", views.PostOfficeView, basename="district-admin")
router.register("basic/setting", views.BasicSettingView, basename="basic-setting")
router.register("free/delivery", views.DeliveryFreeAreaView, basename="free-delivery")
router.register("coupon/user", views.AddCouponToUser, basename="coupon-user")

urlpatterns = [
    path('auth/token/check/', views.login_set_cookie),
    path('auth/get/admin/', views.get_user),
    path('auth/admin/login/', views.admin_login),
    path('product/create/fully/', views.ProductCreateAll.as_view()),
    path('product/list/', views.ProductListView.as_view()),
    path('product/edit/<int:pk>/', views.ProductEditView.as_view()),
    path('product/delete/image/<int:pk>/', views.ProductImageDeleteView.as_view()),
    path('product/add/image/', views.ProductImageAddView.as_view()),
    path('product/update/image/<int:pk>/', views.ProductImageUpdateView.as_view()),
    path('product/update/basic/<int:pk>/', views.ProductBasicUpdateView.as_view()),
    path('product/variation/<int:pk>/', views.ProductVariationUpdateView.as_view()),
    path('product/create/variation/<int:pk>/', views.ProductCreateVariation.as_view()),
    path('product/delete/variation/<int:pk>/', views.ProductDeleteVariation.as_view()),
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view()),
    path('division/district/all/', DivisionAllView.as_view()),
    # get order info
    path('checkout/list/today/', views.OrderTodayList.as_view()),
    path('checkout/list/previous/', views.OrderPreviousList.as_view()),
    path('checkout/single/<slug:checkout_id>/', views.OrderSingle.as_view()),
    path('checkout/update/<slug:checkout_id>/', views.OrderUpdateStatus.as_view()),
    # dashboard
    path('dashboard/basic/info/', views.TodayIncome.as_view()),
    path('top/buying/user/', views.TopBuyingUser.as_view()),
    path('user/all/coupons/', views.UserAllCoupons.as_view()),
]
urlpatterns += router.urls
