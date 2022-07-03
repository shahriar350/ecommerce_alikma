from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from sslcommerz_lib import SSLCOMMERZ

from EcommerceClient.mixins import IsAdminOrReadOnly
from basic_module_app.models import Category, Variation, Collection, Brand, ProductType, UserAddress, \
    Division, Banner
from basic_module_app.serializers import CategorySerializer, VariationSerializer, CollectionSerializer, BrandSerializer, \
    ProductTypeSerializer, UserAddressSerializer, BannerSerializer

from user_app.serializers import DivisionSerializer


class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class VariationView(ModelViewSet):
    serializer_class = VariationSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Variation.objects.all()


class CollectionView(ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Collection.objects.all()


class BrandView(ModelViewSet):
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Brand.objects.all()


class BannerView(ModelViewSet):
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Banner.objects.all()


class ProductTypeView(ModelViewSet):
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = ProductType.objects.all()


class UserAddressView(ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = UserAddress.objects.all()


class DivisionAllView(ListAPIView):
    serializer_class = DivisionSerializer
    queryset = Division.objects.prefetch_related("get_districts").all()


class BannerList(ListAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(trash=False).all()

# class CouponBuyView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication, SessionAuthentication]
#     serializer_class = UserCouponCreateSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         instance = serializer.save()
#         print(instance)
#         setting = {'store_id': settings.SSL_STORE_ID, "store_pass": settings.SSL_STORE_PASSWORD, 'issandbox': True}
#         sslcommez = SSLCOMMERZ(setting)
#         print("hello2")
#         post_body = {'total_amount': instance.coupon.price, 'currency': "BDT", 'tran_id': str(instance.id),
#                      'success_url': settings.HOSTNAME + "/basic/coupon/payment/complete/",
#                      'fail_url': settings.HOSTNAME + "/basic/coupon/payment/failed/",
#                      'cancel_url': settings.HOSTNAME + "/basic/coupon/payment/cancel/", 'emi_option': 0,
#                      'cus_name': instance.user.name,
#                      'cus_email': "None", 'cus_phone': instance.user.phone_number, 'cus_add1': "null",
#                      'cus_city': "null", 'cus_country': "Bangladesh", 'shipping_method': "NO",
#                      'multi_card_name': "",
#                      'num_of_item': 1, 'product_name': "None", 'product_category': "Test Category",
#                      'product_profile': "general", }
#         response = sslcommez.createSession(post_body)
#         print("hello1")
#         return Response(data={
#             'id': instance.id,
#             'coupon': instance.coupon_id,
#             'user': instance.user_id,
#             'payment_url': response['GatewayPageURL'],
#         })
#
#
# class CouponPaymentCompleteView(CreateAPIView):
#     serializer_class = CouponBankSerializer
#     queryset = CouponBank.objects.all()
#
#     def perform_create(self, serializer):
#         serializer = serializer.save()
#         serializer.tran_id.payment = True
#         serializer.tran_id.save()
#         return serializer
#
#
# class CouponPaymentFailedView(APIView):
#     def post(self, request):
#         return Response(data="Your coupon payment is failed. Please try again.", status=status.HTTP_400_BAD_REQUEST)
#
#
# class CouponPaymentCancelView(APIView):
#     def post(self, request):
#         return Response(data="Your coupon payment is canceled. Please try again.", status=status.HTTP_400_BAD_REQUEST)
