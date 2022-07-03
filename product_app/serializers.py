from rest_framework import serializers

from admin_api.serializers import ProductImagesSerializerAdmin
from product_app.models import Product, ProductVariation, ProductImage
from user_app.models import Checkout, CheckoutProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = "__all__"


class ProductMinSerializer(serializers.ModelSerializer):
    get_product_images = ProductImagesSerializerAdmin(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'offer_price',
            'is_offer_valid',
            'first_page_showing_price',
            'get_product_images',
            'show_min_price',
        ]


class ProductAppImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductAppFullSerializer(serializers.ModelSerializer):
    get_product_images = ProductAppImageSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"

