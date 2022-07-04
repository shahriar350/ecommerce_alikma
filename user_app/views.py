import datetime
from decimal import Decimal

from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db.models import Q, Sum, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.timezone import get_current_timezone, get_default_timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from sslcommerz_lib import SSLCOMMERZ

from auth_app.models import User
from basic_module_app.models import Division, Coupon, DeliveryFreeArea, BasicSetting
from basic_module_app.serializers import CouponSerializer
from product_app.models import Product
from user_app.models import Cart, CheckoutPayment, Checkout, CheckoutProduct, CartProduct
from user_app.serializers import CartProductSerializer, CheckoutCreateSerializer, CheckoutPaymentSerializer, \
    DivisionSerializer, CheckoutUserDetails, CartUserSerializer, UserInfoSerializer, OrderHistorySerializer, \
    PasswordResetSerializer, TrackSerializer, RemoveCartSerializer
from django.core.files.storage import default_storage

f = Fernet(settings.ENCRYPT_KEY)


class CartProductView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = CartProductSerializer


class CartList(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = CartUserSerializer

    def get_object(self):
        return Cart.objects.prefetch_related("get_cart_products").filter(completed=False,
                                                                         user=self.request.user).first()


class CartProductRemove(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_object(self):
        cart_product = get_object_or_404(
            CartProduct.objects.filter(cart__completed=False).all(), product_id=self.kwargs.get('product_id'))
        return cart_product


class CartProductCount(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request):
        cart = Cart.objects.prefetch_related("get_cart_products").filter(completed=False,
                                                                         user=request.user).first()
        return Response(data={'count': cart.get_cart_products.count()})


class CartCheckout(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = CheckoutCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = CheckoutCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # get all data
        cart = serializer.validated_data.get("cart", None)
        user = serializer.validated_data.get("user", None)
        coupon = serializer.validated_data.get("coupon", None)
        address = serializer.validated_data.get("address", None)
        total_price = serializer.validated_data.get("total_price", None)
        # init for calc total price of cart
        basic_info = BasicSetting.objects.first()
        total_price = cart.total_price
        delivery_charge = Decimal(0)
        # check if delivery charge free
        if not DeliveryFreeArea.objects.filter(post_office=address.post_office).exists():
            total_price += basic_info.delivery_charge
            delivery_charge += basic_info.delivery_charge
        # check if couple apply in checkout
        if coupon is not None and coupon.check_validate_date and coupon.active:
            total_price -= coupon.reduce_money
        # save checkout init
        checkout, _ = Checkout.objects.get_or_create(cart=cart, defaults={
            "address": address, "coupon": coupon, "user": request.user,
            "total_price": total_price, "delivery_charge": delivery_charge, "save_money": cart.total_saving
        })

        for cart_product in cart.get_cart_products.all():
            CheckoutProduct.objects.create(checkout=checkout, product=cart_product.product,
                                           single_price=cart_product.final_price,
                                           quantity=cart_product.quantity, offer_price=cart_product.get_offer_price,
                                           variation=cart_product.variation)

        setting = {'store_id': settings.SSL_STORE_ID, 'store_pass': settings.SSL_STORE_PASSWORD, 'issandbox': True}
        sslcommez = SSLCOMMERZ(setting)
        post_body = {'total_amount': total_price, 'currency': "BDT", 'tran_id': str(checkout.id),
                     'success_url': settings.SSL_HOST_SUCCESS,
                     'fail_url': settings.SSL_HOST_FAIL, 'cancel_url': settings.SSL_HOST_CANCEL, 'emi_option': 0,
                     'cus_name': user.name,
                     'cus_email': "None", 'cus_phone': user.phone_number, 'cus_add1': address.full_address,
                     'cus_city': address.district.name, 'cus_country': "Bangladesh", 'shipping_method': "NO",
                     'multi_card_name': "",
                     'num_of_item': 1, 'product_name': "None", 'product_category': "Test Category",
                     'product_profile': "general", }
        response = sslcommez.createSession(post_body)
        return Response(data=response['GatewayPageURL'])
        # return Response(status=status.HTTP_200_OK)


class PaymentSuccessSSL(CreateAPIView):
    serializer_class = CheckoutPaymentSerializer
    queryset = CheckoutPayment.objects.all()

    def perform_create(self, serializer):
        serializer = serializer.save()
        serializer.tran_id.order_status = 1
        serializer.tran_id.save()
        serializer.tran_id.cart.completed = 1
        serializer.tran_id.cart.save()
        return serializer


@csrf_exempt
@api_view(['GET', 'POST'])
def payment_success_ssl(request):
    raise ValueError(request.data)


@csrf_exempt
def payment_fail_ssl(request):
    print(request.POST)


@csrf_exempt
def payment_cancel_ssl(request):
    print(request.POST)


@csrf_exempt
def payment_ipn_ssl(request):
    pass


class SearchCouponView(ListAPIView):
    serializer_class = CouponSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    # def filter_queryset(self, queryset):
    def get_queryset(self):
        if 'name' in self.request.GET:
            coupons = Coupon.objects.filter(trash=False)
            ids = []
            myCoupon = coupons.all()
            for i in myCoupon:
                if i.validate_date >= datetime.datetime.now(tz=get_default_timezone()):
                    ids.append(i.id)
            return coupons.filter(id__in=ids).all()
        else:
            return Coupon.objects.none()


# def finalize_response(self, request, response, *args, **kwargs):
#     print(response)
class OrderList(ListAPIView):
    serializer_class = CheckoutUserDetails
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Checkout.objects.prefetch_related("get_checkout_products__product").filter(user=self.request.user).all()


class UserInfoView(RetrieveAPIView, CreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get(self, request):
        user = User.objects.prefetch_related('get_user_checkout__get_checkout_products').filter(
            pk=request.user.id).annotate(total_buy=Sum('get_user_checkout__total_price'),
                                         total_save=Sum('get_user_checkout__save_money'),
                                         total_checkout=Sum(
                                             'get_user_checkout__get_checkout_products__quantity')).first()

        return Response(data=UserInfoSerializer({
            'id': user.id,
            'name': user.name,
            'phone_number': user.phone_number,
            'image': user.image,
            'total_saving': user.total_save,
            'total_cost': user.total_buy,
            'total_checkout_products': user.total_checkout,
        }, context={'request': request}).data)

    def post(self, request):
        user = User.objects.filter(
            pk=request.user.id).first()
        data = request.data
        if 'name' in data and data['name'] is not None:
            user.name = data.get('name')
        if 'image' in data and data['image'] is not None:
            user.image.delete()
            user.image = data.get('image')
        user.save()
        return Response(data=UserInfoSerializer({
            'id': user.id,
            'name': user.name,
            'phone_number': user.phone_number,
            'image': user.image,
        }, context={'request': request}).data)


class OrderHistoryView(ListAPIView):
    serializer_class = OrderHistorySerializer

    def get_queryset(self):
        return Checkout.objects.prefetch_related("get_checkout_products__product").filter(user=self.request.user).all()


class UserPasswordReset(CreateAPIView):
    serializer_class = PasswordResetSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class OrderTrackView(RetrieveAPIView):
    serializer_class = TrackSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Checkout.objects.filter(id=self.kwargs.get('order_id')).first()
