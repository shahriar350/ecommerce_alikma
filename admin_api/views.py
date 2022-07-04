import datetime
import uuid
from decimal import Decimal
from typing import Optional

import ujson
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Prefetch, Count, Sum
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
from django_filters import filters
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, \
    UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from EcommerceClient.mixins import PageNumberPaginationWithCount, IsAdminOrReadOnly
from admin_api.serializers import UserSerializerAdmin, SingleUserSerializerAdmin, \
    UserAddressSerializerAdmin, ProductTypeSerializerAdmin, BrandSerializerAdmin, CollectionSerializerAdmin, \
    VariationSerializerAdmin, \
    CategorySerializerAdmin, CouponSerializerAdmin, CreateProductAllAdmin, CreateCategorySerializerAdmin, \
    ProductVariationSerializerAdmin, CreateVariationSerializerAdmin, ProductCreateSerializerAdmin, \
    FullProductSerializerAdmin, \
    ProductImageSerializerAdmin, \
    ProductBasicUpdateSerializerAdmin, ProductVariationUpdateSerializerAdmin, \
    ProductVariationValueUpdateSerializerAdmin, \
    DivisionAdminSerializerAdmin, DistrictAdminSerializerAdmin, BasicSettingSerializerAdmin, \
    DeliveryFreeAreaSerializerAdmin, OrderListAdminSerializer, OrderAdminSerializer, CheckoutProdAdminSerializer, \
    TopUserSerializerAdmin, UserCouponAdminSerializer, UserInfoSerializerAdmin, UserAllCouponsSerializer
from auth_app.serializers import UserSerializer
from basic_module_app.models import UserAddress, ProductType, Brand, Collection, Variation, \
    Category, Coupon, District, Division, PostOffice, BasicSetting, DeliveryFreeArea, UserCoupon, Banner
from basic_module_app.serializers import BannerSerializer
from product_app.models import ProductImage, Product, ProductVariationValues, ProductVariation
from product_app.serializers import ProductSerializer
from user_app.models import Checkout, CheckoutProduct
from user_app.serializers import DistrictSerializer, DivisionSerializer, PostofficeSerializer
from auth_app.models import User


@authentication_classes([SessionAuthentication])
@ensure_csrf_cookie
@api_view(['GET'])
def login_set_cookie(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)


@authentication_classes([SessionAuthentication])
@api_view(['GET'])
def get_user(request):
    if request.method == "GET":
        if request.user.is_authenticated and request.user.is_superuser:
            return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def admin_login(request):
    if request.method == 'POST':
        serializer = SingleUserSerializerAdmin(data=request.data)
        serializer.is_valid(raise_exception=True)
        number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        user = authenticate(username=number, password=password)
        if user and user.is_superuser:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            raise ValidationError('Please provide correct credential')


# basic module start
class CategoryView(ModelViewSet):
    serializer_class = CategorySerializerAdmin
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]
    # def list(self, request, *args, **kwargs):
    #     queryset = Category.objects.filter(level=0)
    #     return Response(data=self.serializer_class(queryset, many=True).data)


class VariationView(ModelViewSet):
    serializer_class = VariationSerializerAdmin
    permission_classes = [IsAdminUser]
    queryset = Variation.objects.all()
    authentication_classes = [SessionAuthentication]


class UserView(ModelViewSet):
    serializer_class = UserInfoSerializerAdmin
    queryset = User.objects.all()
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAdminUser]
    pagination_class = PageNumberPaginationWithCount
    filter_backends = [SearchFilter]
    search_fields = ['name', 'phone_number']

    def perform_create(self, serializer):
        if "password" in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        else:
            raise ValidationError({"password": ['Password is required.']})
        print(serializer.validated_data)
        serializer.save()

    def perform_update(self, serializer):
        if "password" in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()


class CollectionView(ModelViewSet):
    serializer_class = CollectionSerializerAdmin
    permission_classes = [IsAdminUser]
    queryset = Collection.objects.all()
    authentication_classes = [SessionAuthentication]


class BrandView(ModelViewSet):
    serializer_class = BrandSerializerAdmin
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    authentication_classes = [SessionAuthentication]


class ProductTypeView(ModelViewSet):
    serializer_class = ProductTypeSerializerAdmin
    permission_classes = [IsAdminUser]
    queryset = ProductType.objects.all()
    authentication_classes = [SessionAuthentication]


class CouponView(ModelViewSet):
    serializer_class = CouponSerializerAdmin
    permission_classes = [IsAdminUser]
    queryset = Coupon.objects.all()
    authentication_classes = [SessionAuthentication]


class BannerView(ModelViewSet):
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Banner.objects.all()


class UserAddressView(ModelViewSet):
    serializer_class = UserAddressSerializerAdmin
    permission_classes = [IsAdminUser]
    queryset = UserAddress.objects.all()
    authentication_classes = [SessionAuthentication]


class DistrictView(ModelViewSet):
    serializer_class = DistrictAdminSerializerAdmin
    permission_classes = [IsAdminUser]
    queryset = District.objects.all()
    authentication_classes = [SessionAuthentication]


class DivisionView(ModelViewSet):
    serializer_class = DivisionAdminSerializerAdmin
    permission_classes = [IsAdminUser]
    queryset = Division.objects.all()
    authentication_classes = [SessionAuthentication]


class PostOfficeView(ModelViewSet):
    serializer_class = PostofficeSerializer
    permission_classes = [IsAdminUser]
    queryset = PostOffice.objects.all()
    authentication_classes = [SessionAuthentication]


# basic module end

# create product
class ProductCreateAll(CreateAPIView):
    serializer_class = ProductCreateSerializerAdmin
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        data = request.data
        basic_get = data.get('basic', None)
        if basic_get is None:
            raise ValidationError("Basic information is mandatory.")
        basic = ujson.loads(basic_get)
        primary_image = request.data.get('primary_image', None)
        if primary_image is None:
            raise ValidationError("A primary image is mandatory.")
        with transaction.atomic():
            product = ProductCreateSerializerAdmin(data=basic)
            product.is_valid(raise_exception=True)
            prod = product.save()
            variation_get = data.get('variations', None)
            if variation_get is not None:
                variations = ujson.loads(variation_get)
                variance_images = request.data.getlist('variance_images', None)
                for index, variation in enumerate(variations):
                    try:
                        img = variance_images[index]
                    except Exception as e:
                        img = None

                    variation_ser = CreateVariationSerializerAdmin(data={
                        'product': prod.id,
                        'sku': variation['sku'],
                        'quantity': variation['quantity'],
                        'product_price': variation['product_price'],
                        'selling_price': variation['selling_price'],
                        'image': img,
                        'get_product_variation_values': variation['get_product_variation_values']
                    })

                    variation_ser.is_valid(raise_exception=True)

                    variation_ser.save()
            # save product image
            ProductImage.objects.create(image=primary_image, product=prod,
                                        primary=True)
            # save product additional image
            images = request.data.getlist('images', None)
            if images is not None:
                for i in images:
                   
                    ProductImage.objects.create(image=i, product=prod)
            return Response(status=status.HTTP_201_CREATED)


class ProductListView(ListAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]
    queryset = Product.objects.prefetch_related(
        Prefetch("get_product_images", queryset=ProductImage.objects.filter(primary=True)))
    serializer_class = FullProductSerializerAdmin
    depth = 2


class ProductEditView(RetrieveUpdateDestroyAPIView):
    serializer_class = FullProductSerializerAdmin
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]


class ProductImageDeleteView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def delete(self, request, pk, format=None):
        product_image = ProductImage.objects.get(id=pk)
        product_image.delete()
        return Response(status=status.HTTP_200_OK)


class ProductImageAddView(CreateAPIView):
    serializer_class = ProductImageSerializerAdmin
    queryset = ProductImage.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]


class ProductImageUpdateView(UpdateAPIView):
    serializer_class = ProductImageSerializerAdmin
    queryset = ProductImage.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def perform_update(self, serializer):
        if serializer.validated_data.get("primary"):
            product_image = ProductImage.objects.get(id=self.kwargs['pk'])
            product = Product.objects.prefetch_related("get_product_images").get(id=product_image.product_id)
            for i in product.get_product_images.all():

                if i.primary:
                    i.primary = False
                    i.save()
        serializer.save()


class ProductBasicUpdateView(UpdateAPIView):
    serializer_class = ProductBasicUpdateSerializerAdmin
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]


class ProductVariationUpdateView(UpdateAPIView):
    serializer_class = ProductVariationUpdateSerializerAdmin
    queryset = ProductVariation.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]


class ProductCreateVariation(CreateAPIView):
    serializer_class = CreateVariationSerializerAdmin
    queryset = ProductVariation.objects.none()
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        product_id = kwargs['pk']
        data = request.data
        variation_ids = []
        variation_get = data.get('variations', None)
        if variation_get is not None:
            variations = ujson.loads(variation_get)
            variance_images = request.data.getlist('variance_images', None)
            for index, variation in enumerate(variations):
                variation_ser = CreateVariationSerializerAdmin(data={
                    'product': product_id,
                    'sku': variation['sku'],
                    'quantity': variation['quantity'],
                    'product_price': variation['product_price'],
                    'selling_price': variation['selling_price'],
                    'image': variance_images[index] if len(variance_images) > 0 else None,
                    'get_product_variation_values': variation['get_product_variation_values']
                })
                variation_ser.is_valid(raise_exception=True)

                save = variation_ser.save()
        all_variations = ProductVariation.objects.prefetch_related("get_product_variation_values__variation").filter(
            product_id=product_id).all()
        return Response(
            data=ProductVariationSerializerAdmin(all_variations, many=True, context={'request': request}).data)


class ProductDeleteVariation(DestroyAPIView):
    serializer_class = ProductVariationSerializerAdmin
    queryset = ProductVariation.objects.prefetch_related("get_product_variation_values__variation").all()
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]


class ProductDeleteView(DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]


class BasicSettingView(ModelViewSet):
    serializer_class = BasicSettingSerializerAdmin
    queryset = BasicSetting.objects.all()
    # pass


class DeliveryFreeAreaView(ModelViewSet):
    serializer_class = DeliveryFreeAreaSerializerAdmin
    queryset = DeliveryFreeArea.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]


# order informations
class OrderTodayList(ListAPIView):
    serializer_class = OrderListAdminSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        date = datetime.date.today()
        return Checkout.objects.filter(date_created__date=date).annotate(
            total_products=Count('get_checkout_products', distinct=True)).order_by('date_created').all()


class OrderPreviousList(ListAPIView):
    serializer_class = OrderListAdminSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        date = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        return Checkout.objects.filter(date_created__lt=date).annotate(
            total_products=Count('get_checkout_products', distinct=True)).order_by('date_created').all()


class OrderSingle(RetrieveAPIView):
    serializer_class = OrderAdminSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def get_object(self):
        return Checkout.objects.prefetch_related("get_checkout_payment", "get_checkout_products__product",
                                                 "get_checkout_products__variation__get_variation_cart_products").get(
            id=self.kwargs.get('checkout_id'))


class OrderUpdateStatus(UpdateAPIView):
    serializer_class = OrderListAdminSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def get_object(self):
        return Checkout.objects.get(id=self.kwargs.get('checkout_id'))


class TodayIncome(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        today = datetime.date.today()
        total = Decimal(0)
        total_today = Decimal(0)
        checkouts = Checkout.objects.all()
        total_products = Product.objects.count()
        total_user = User.objects.count()
        top_products = CheckoutProduct.objects.values("product_id", "product__name", "quantity").annotate(
            product_count=Count('product_id'), product_sell_quantity=Sum("quantity")).order_by('-product_count')[:10]

        chart_line_checkout_sell_progress = [['Date', 'Sales product', 'Seles quantity of product'],
                                             [request.user.date_joined.date(), 0, 0]]
        for checkout in checkouts:

            if checkout.date_created.date() == chart_line_checkout_sell_progress[-1][0]:

                chart_line_checkout_sell_progress[-1][1] += checkout.get_checkout_products.count()
                chart_line_checkout_sell_progress[-1][2] += checkout.get_checkout_products.values('quantity').annotate(
                    total_sales=Sum('quantity')).aggregate(total=Sum('total_sales'))['total']

            else:

                chart_line_checkout_sell_progress.append(
                    [checkout.date_created.date(), checkout.get_checkout_products.count(),
                     checkout.get_checkout_products.values('quantity').annotate(total_sales=Sum('quantity')).aggregate(
                         total=Sum('total_sales'))['total']])
            if checkout.date_created.day == today.day and checkout.date_created.month == today.month \
                    and checkout.date_created.year == today.year:
                total_today += checkout.total_price
            total += checkout.total_price

        return Response(data={
            'total_income_today': total_today,
            'total_income': total,
            'total_products': total_products,
            'total_users': total_user,
            'top_selling_products': top_products,
            "chart_line_checkout_sell_progress": chart_line_checkout_sell_progress,
        }, status=status.HTTP_200_OK)


class TopBuyingUser(ListAPIView):
    serializer_class = TopUserSerializerAdmin

    def get_queryset(self):
        return User.objects.annotate(total_buy=Count('get_user_checkout')).order_by('-total_buy').all()[:10]


class AddCouponToUser(ModelViewSet):
    serializer_class = UserCouponAdminSerializer
    queryset = UserCoupon.objects.all()


class UserAllCoupons(ListAPIView):
    serializer_class = UserAllCouponsSerializer
    queryset = User.objects.prefetch_related('get_user_coupons__coupon').all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'phone_number']
