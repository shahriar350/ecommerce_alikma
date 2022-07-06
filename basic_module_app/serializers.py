from rest_framework import serializers

from basic_module_app.models import Category, Variation, Collection, Brand, ProductType, UserAddress, \
    Coupon, UserCoupon, Banner, Division, District, PostOffice


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAddress
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


#
# class UserCouponCreateSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     payment_url = serializers.CharField(max_length=255,allow_null=True, required=False,read_only=True)
#
#     class Meta:
#         model = UserCoupon
#         fields = [
#             'id',
#             'coupon',
#             'user',
#             'payment_url',
#         ]
#
#
# class CouponBankSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CouponBank
#         fields = "__all__"

class PostOfferInnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOffice
        fields = "__all__"


class DistrictInnerSerializer(serializers.ModelSerializer):
    get_district_post_offices = PostOfferInnerSerializer(many=True)

    class Meta:
        model = District
        fields = "__all__"


class DivisionInnerSerializer(serializers.ModelSerializer):
    get_districts = DistrictInnerSerializer(many=True)

    class Meta:
        model = Division
        fields = "__all__"
