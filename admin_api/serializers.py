from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from auth_app.serializers import UserSerializer
from basic_module_app.models import Coupon, UserAddress, ProductType, Brand, Collection, Variation, \
    Category, District, Division, PostOffice, BasicSetting, DeliveryFreeArea, UserCoupon
from product_app.models import Product, ProductImage, ProductVariation, ProductVariationValues
from user_app.models import Checkout, CheckoutProduct, CheckoutPayment

User = get_user_model()


class UserSerializerAdmin(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'phone_number']

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            name=validated_data['name'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
        )
        return user


class UserInfoSerializerAdmin(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    # def validate_phone_number(self, data):
    #     print(data)
    #     if User.objects.filter(phone_number=data).count() > 0:
    #         raise ValidationError("This phone number is already used.")
    #     if len(data) != 11:
    #         raise ValidationError("This phone number must be 11 digit.")
    #     if not isinstance(data, int):
    #         raise ValidationError("This phone number must be digit number.")
    #
    #     return data


class SingleUserSerializerAdmin(serializers.Serializer):
    phone_number = serializers.CharField(min_length=11, max_length=11)
    password = serializers.CharField()


class CategorySerializerAdmin(serializers.ModelSerializer):
    # leaf_nodes = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    # def get_leaf_nodes(self, obj):
    #     return CategorySerializer(obj.get_children(), many=True).data


class VariationSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = "__all__"


class CollectionSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


class BrandSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductTypeSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"


class UserAddressSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"


# print(validated_data['district'] is None)


class CouponSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class ProductVariationValuesSerializerAdmin(serializers.ModelSerializer):
    variation = VariationSerializerAdmin()

    class Meta:
        model = ProductVariationValues
        fields = [
            'product_variation',
            'variation',
            'title',
        ]


class ProductVariationSerializerAdmin(serializers.ModelSerializer):
    get_product_variation_values = ProductVariationValuesSerializerAdmin(many=True)

    class Meta:
        model = ProductVariation
        fields = [
            'id',
            'product',
            'sku',
            'quantity',
            'product_price',
            'selling_price',
            'image',
            'get_product_variation_values',
        ]


class ProductImagesSerializerAdmin(serializers.ModelSerializer):
    # image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = "__all__"

    # def get_image_url(self, obj):
    #     imagekit_url = imagekit.url({
    #         "path": obj.image,
    #         "url_endpoint": settings.IMAGEKIT_ENDPOINT,
    #     })
    #     return imagekit_url


class ProductCreateSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class BasicSerializerAdmin(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    sky = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    product_price = serializers.DecimalField(max_digits=100, decimal_places=2, default=0)
    selling_price = serializers.DecimalField(max_digits=100, decimal_places=2, default=0)
    quantity = serializers.IntegerField(default=0)
    description = serializers.CharField()
    offer_price = serializers.DecimalField(max_digits=100, decimal_places=2, default=0)
    offer_start = serializers.DateField(allow_null=True)
    offer_end = serializers.DateField(allow_null=True)
    next_stock_date = serializers.DateField(allow_null=True)
    type = serializers.PrimaryKeyRelatedField(queryset=ProductType.objects.all())


class CreateCategorySerializerAdmin(serializers.Serializer):
    data = serializers.IntegerField()

    def validate_data(self, data):
        return Category.objects.get(id=data)


class CreateCollectionSerializerAdmin(serializers.Serializer):
    data = serializers.IntegerField()

    def validate_data(self, data):
        return Collection.objects.get(id=data)


class CreateVariationValueAdmin(serializers.ModelSerializer):
    class Meta:
        model = ProductVariationValues
        fields = [
            'id',
            'variation',
            'title',
        ]


class CreateVariationSerializerAdmin(serializers.ModelSerializer):
    get_product_variation_values = CreateVariationValueAdmin(many=True)

    class Meta:
        model = ProductVariation
        fields = [
            'id',
            'product',
            'sku',
            'quantity',
            'product_price',
            'selling_price',
            'image',
            'get_product_variation_values'
        ]

    def create(self, validated_data):
        with transaction.atomic():
            print(validated_data['image'])
            values = validated_data.pop("get_product_variation_values")
            variation = ProductVariation.objects.create(**validated_data)

            for i in values:
                val = ProductVariationValues()
                val.variation = i['variation']
                val.product_variation = variation
                val.title = i['title']
                val.save()
        return ProductVariation.objects.none()


class CreateProductAllAdmin(serializers.Serializer):
    basic = BasicSerializerAdmin(many=True)
    categories = CreateCategorySerializerAdmin(many=True)
    collections = CreateCollectionSerializerAdmin(many=True)
    variations = CreateVariationSerializerAdmin(many=True)
    primary_image = serializers.ImageField()
    images = serializers.ImageField()
    variance_images = serializers.ImageField()


class FullProductSerializerAdmin(serializers.ModelSerializer):
    get_product_images = ProductImagesSerializerAdmin(many=True)
    get_product_variations = ProductVariationSerializerAdmin(many=True)

    # categories = serializers.StringRelatedField(many=True)
    # collections = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'sku',
            'quantity',
            'product_price',
            'selling_price',
            'offer_price',
            'offer_start',
            'offer_end',
            'active',
            'next_stock_date',
            'description',
            'brand',
            'type',
            'categories',
            'collections',
            'date_created',
            'trash',
            'get_product_images',
            'get_product_variations',
        ]


#
# class ProductAdminAllSerializer(serializers.ModelSerializer):
#     get_product_images = ProductImagesSerializer(many=True)
#     get_product_variations = ProductVariationSerializer(many=True)
#
#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'name',
#             'slug',
#             'sku',
#             'quantity',
#             'product_price',
#             'selling_price',
#             'offer_price',
#             'offer_start',
#             'offer_end',
#             'active',
#             'next_stock_date',
#             'description',
#             'brand',
#             'type',
#             'categories',
#             'collections',
#             'get_product_images',
#             'get_product_variations',
#         ]
class ProductImageSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductBasicUpdateSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductVariationUpdateSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = "__all__"


class ProductVariationValueUpdateSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = ProductVariationValues
        fields = "__all__"


class PostOfficeAdminSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = PostOffice
        fields = "__all__"


class UserAddressAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['full_address']


class DistrictAdminSerializerAdmin(serializers.ModelSerializer):
    division_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = District
        fields = "__all__"

    def get_division_name(self, obj):
        return obj.division.name


class DistrictAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class DivisionAdminSerializerAdmin(serializers.ModelSerializer):
    get_districts = DistrictAdminSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Division
        fields = (
            'id',
            'name',
            'get_districts',
        )


class BasicSettingSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = BasicSetting
        fields = "__all__"

    def create(self, validated_data):
        if BasicSetting.objects.exists():
            raise ValidationError("One data is already exists.")
        else:
            return BasicSetting.objects.create(**validated_data)


class DeliveryFreeAreaSerializerAdmin(serializers.ModelSerializer):
    post_office_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DeliveryFreeArea
        fields = "__all__"

    def get_post_office_name(self, obj):
        return obj.post_office.name


class CheckoutProductMainInfoAdminSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.UUIDField()


class CheckoutProductVariationValueMainInfoAdminSerializer(serializers.ModelSerializer):
    variation = VariationSerializerAdmin()

    class Meta:
        model = ProductVariationValues
        fields = "__all__"


class CheckoutProductVariationMainInfoAdminSerializer(serializers.ModelSerializer):
    get_product_variation_values = CheckoutProductVariationValueMainInfoAdminSerializer(many=True)

    class Meta:
        model = ProductVariation
        fields = "__all__"


class CheckoutProductListAdminSerializer(serializers.ModelSerializer):
    product = CheckoutProductMainInfoAdminSerializer()
    variation = CheckoutProductVariationMainInfoAdminSerializer()

    class Meta:
        model = CheckoutProduct
        fields = "__all__"


class UserShortAdminSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=11)


class OrderListAdminSerializer(serializers.ModelSerializer):
    total_products = serializers.IntegerField(read_only=True)

    class Meta:
        model = Checkout
        fields = "__all__"


class CheckoutPaymentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutPayment
        fields = "__all__"


class OrderAdminSerializer(serializers.ModelSerializer):
    user = UserShortAdminSerializer()
    get_checkout_products = CheckoutProductListAdminSerializer(many=True)
    address = UserAddressAdminSerializer()
    get_checkout_payment = CheckoutPaymentAdminSerializer()

    class Meta:
        model = Checkout
        fields = "__all__"


class CheckoutProdAdminSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CheckoutProduct
        fields = "__all__"


class TopUserSerializerAdmin(serializers.ModelSerializer):
    total_buy = serializers.IntegerField(read_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'phone_number',
            'image',
            'total_buy',
        ]


class UserCouponAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCoupon
        fields = "__all__"

    def validate(self, attr):
        coupon = attr.get('coupon')
        user = attr.get('user')
        if UserCoupon.objects.filter(coupon=coupon, user=user, used=False).count() > 0:
            raise ValidationError("User have already same unused coupon.")
        return attr


class UserCouponV1AdminSerializer(serializers.ModelSerializer):
    coupon = CouponSerializerAdmin()

    class Meta:
        model = UserCoupon
        fields = "__all__"


class UserAllCouponsSerializer(serializers.ModelSerializer):
    get_user_coupons = UserCouponV1AdminSerializer(many=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'phone_number',
            'get_user_coupons',
        ]
