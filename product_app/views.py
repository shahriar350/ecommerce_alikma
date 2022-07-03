from django.conf import settings
from django.db.models import Prefetch, Q
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from EcommerceClient.mixins import IsAdminOrReadOnly
from product_app.filters.product_filter_by_price_range import ProductPriceRangeFilter
from product_app.models import Product, ProductVariation, ProductImage
from product_app.serializers import ProductSerializer, ProductVariationSerializer, ProductMinSerializer, \
    ProductAppFullSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from user_app.models import Checkout


class ProductList(ListAPIView):
    serializer_class = ProductMinSerializer
    queryset = Product.objects.prefetch_related(
        Prefetch('get_product_images',
                 queryset=ProductImage.objects.filter(primary=True).all())) \
        .filter(active=True, trash=False).all()


class ProductFullList(ListAPIView):
    serializer_class = ProductAppFullSerializer
    queryset = Product.objects.prefetch_related('get_product_images') \
        .filter(active=True, trash=False).all()


class ProductBasicCRUD(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class ProductOperation(ModelViewSet):
    serializer_class = ProductAppFullSerializer
    queryset = Product.objects.prefetch_related(
        Prefetch("get_product_images", queryset=ProductImage.objects.filter(primary=True).all())).filter(
        active=True).all()

    def get_object(self):
        return Product.objects.filter(active=True, id=self.kwargs.get('pk')).first()

    permission_classes = [IsAdminOrReadOnly]


class ProductVariationCRUD(ModelViewSet):
    serializer_class = ProductVariationSerializer
    queryset = ProductVariation.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = ProductVariationSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ProductFilterByBrand(ListAPIView):
    serializer_class = ProductMinSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch("get_product_images", queryset=ProductImage.objects.filter(primary=True).all())).filter(
            Q(brand_id=self.kwargs.get('id')) & Q(active=True) & Q(trash=False)).distinct()


class ProductFilterByCategory(ListAPIView):
    serializer_class = ProductMinSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch("get_product_images", queryset=ProductImage.objects.filter(primary=True).all())).filter(
            Q(categories__id=self.kwargs.get('id')) & Q(active=True) & Q(trash=False)).distinct()


class ProductFilterByCollections(ListAPIView):
    serializer_class = ProductMinSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch("get_product_images", queryset=ProductImage.objects.filter(primary=True).all())).filter(
            Q(collections__id=self.kwargs.get('id')) & Q(active=True) & Q(trash=False)).distinct()


class ProductFilterByType(ListAPIView):
    serializer_class = ProductMinSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch("get_product_images", queryset=ProductImage.objects.filter(primary=True).all())).filter(
            Q(type_id=self.kwargs.get('id')) & Q(active=True) & Q(trash=False)).distinct()


class UserSearchListView(ListAPIView):

    def get_queryset(self):
        if not self.request.GET._mutable:
            self.request.GET._mutable = True
        if self.request.GET.get('categories') == '':
            del self.request.GET['categories']
        if self.request.GET.get('collections') == '':
            del self.request.GET['collections']

        return Product.objects.prefetch_related(
            Prefetch("get_product_images", queryset=ProductImage.objects.filter(primary=True).all())).filter(
            active=True).all()

    serializer_class = ProductMinSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = ProductPriceRangeFilter
    search_fields = ['name']
    # filterset_fields = ['brand',
    #                     'type',
    #                     'categories',
    #                     'collections',"show_min_price__range"]


class TopSellingProduct(ListAPIView):
    serializer_class = ProductMinSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch("get_product_images", queryset=ProductImage.objects.filter(primary=True).all())).filter(
            active=True).all()
