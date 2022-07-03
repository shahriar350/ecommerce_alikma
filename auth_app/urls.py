from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("registration", views.UserRegistration, basename="income-head")
urlpatterns = [
    path('send/otp/', views.SendOTPView.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('admin/login/', views.AdminLoginPageView.as_view(), name='admin.login'),
    path('logout/', views.LogoutUser.as_view()),
    path('check/token/', views.login_set_cookie),
    # path('registration/', views.UserRegistration.as_view()),
]
urlpatterns += router.urls
