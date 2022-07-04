import datetime

from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from basic_module_app.models import UserAddress, Coupon, District, Division, PostOffice
from product_app.models import Product, ProductVariation, ProductVariationValues
from product_app.serializers import ProductSerializer, ProductMinSerializer
from user_app.models import Cart, CartProduct, Checkout, CheckoutPayment, CheckoutProduct

User = get_user_model()
f = Fernet(settings.ENCRYPT_KEY)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class PostofficeSerializer(serializers.ModelSerializer):
    division_name = serializers.SerializerMethodField(read_only=True)
    district_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostOffice
        fields = "__all__"

    def get_division_name(self, obj):
        return obj.division.name

    def get_district_name(self, obj):
        return obj.district.name


class DivisionSerializer(serializers.ModelSerializer):
    get_districts = DistrictSerializer(many=True)

    class Meta:
        model = Division
        fields = (
            'id',
            'name',
            'get_districts',
        )


class CartProductSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(trash=False, active=True).all())
    quantity = serializers.IntegerField(min_value=1)
    variation = serializers.PrimaryKeyRelatedField(queryset=ProductVariation.objects.all(),
                                                   allow_empty=True, allow_null=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        if data['variation'] is not None:
            if data['variation'].product.id != data['product'].id:
                raise ValidationError({'variation': ["Variation is not a variation of this product"]})
        return data

    def create(self, validated_data):
        product = validated_data.get('product', None)
        quantity = validated_data.get('quantity', None)
        variation = validated_data.get('variation', None)
        user = validated_data.get('user', None)
        cart, _ = Cart.objects.get_or_create(user=user, completed=False, trash=False)
        cart_product, created = CartProduct.objects.get_or_create(product=product, cart=cart,
                                                                  defaults={'quantity': quantity,
                                                                            'variation': variation})
        # if product is already in db, update quantity and variation below
        if not created:
            cart_product.quantity = cart_product.quantity + quantity
            cart_product.variation = variation
            cart_product.save()
        return validated_data


class CartProductUserSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = "__all__"


class CartUserSerializer(serializers.ModelSerializer):
    get_cart_products = CartProductUserSerializer(many=True)

    class Meta:
        model = Cart
        fields = "__all__"


class RemoveCartSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(active=True).all())


class CheckoutCreateSerializer(serializers.Serializer):
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.filter(trash=False, completed=False).all())
    address = serializers.PrimaryKeyRelatedField(queryset=UserAddress.objects.all())
    coupon = serializers.PrimaryKeyRelatedField(queryset=Coupon.objects.all(), allow_empty=True,
                                                allow_null=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_price = serializers.DecimalField(decimal_places=2, max_digits=100, default=0)

    def validate_cart(self, data):
        if data.completed:
            raise ValidationError("This cart is already completed.")
        return data

    def validate(self, data):
        if data['cart'].user_id != data['user'].id:
            raise ValidationError({'cart': ['Only target user can purchase his/her cart.']})
        if data['address'].user_id != data['user'].id:
            raise ValidationError({'address': ['Please provide this user address.']})
        return data


'''
{'tran_id': ['48753d76-545e-4a94-ae13-136d1e306ce6'], 
'val_id': ['22040923455FxWozvet0dehleE'], 'amount': ['21.00'], 'card_type': ['NAGAD-Nagad'], 
'store_amount': ['20.48'], 'card_no': [''], 'bank_tran_id': ['22040923455C0JCqjeLHuUG2J7'], 'status': ['VALID'], 
'tran_date': ['2022-04-09 02:34:49'], 'error': [''], 'currency': ['BDT'], 'card_issuer': ['Nagad'], 
'card_brand': ['MOBILEBANKING'], 'card_sub_brand': ['Classic'], 'card_issuer_country': ['Bangladesh'], 
'card_issuer_country_code': ['BD'], 'store_id': ['test5ee312b22782a'], 'verify_sign': ['0e4fcfb8fce20e11378098f2f5552d0d'],
 'verify_key': ['amount,bank_tran_id,base_fair,card_brand,card_issuer,card_issuer_country,card_issuer_country_code,card_no,card_sub_brand,card_type,currency,currency_amount,currency_rate,currency_type,error,risk_level,risk_title,status,store_amount,store_id,tran_date,tran_id,val_id,value_a,value_b,value_c,value_d'], 
 'verify_sign_sha2': ['20764a0220ff2ceb0ad9c9f385511cc78889e9b2af2714fad12583e06c8d437f'], 'currency_type': ['BDT'],
  'currency_amount': ['21.00'], 'currency_rate': ['1.0000'], 'base_fair': ['0.00'], 'value_a': ['1'], 'value_b': ['1'], 
  'value_c': ['1234'], 'value_d': ['uuid'], 'subscription_id': [''], 'risk_level': ['0'], 'risk_title': ['Safe']}

'''


class CheckoutPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutPayment
        fields = "__all__"


class CheckoutProductUserProducts(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CheckoutProduct
        fields = "__all__"


class CheckoutUserDetails(serializers.ModelSerializer):
    get_checkout_products = CheckoutProductUserProducts(many=True)

    class Meta:
        model = Checkout
        fields = "__all__"


class UserInfoSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=255)
    image = serializers.ImageField(allow_empty_file=True)
    total_checkout_products = serializers.IntegerField(default=0, required=False, allow_null=True)
    total_saving = serializers.DecimalField(default=0, max_digits=100, decimal_places=2, required=False,
                                            allow_null=True)
    total_cost = serializers.DecimalField(default=0, max_digits=100, decimal_places=2, required=False, allow_null=True)


class OrderProductsSerializer(serializers.ModelSerializer):
    product = ProductMinSerializer()

    class Meta:
        model = CheckoutProduct
        fields = "__all__"


class OrderHistorySerializer(serializers.ModelSerializer):
    get_checkout_products = OrderProductsSerializer(many=True)

    class Meta:
        model = Checkout
        fields = "__all__"


class PasswordResetSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    previous_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        user = attrs.get('user')
        previous_password = attrs.get('previous_password')
        new_password = attrs.get('new_password')
        if check_password(previous_password, user.password) is False:
            raise ValidationError({"previous_password": ["Invalid password."]})
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        new_password = validated_data.get('new_password')
        user.password = make_password(new_password)
        user.updated_at = datetime.datetime.now()
        user.save()
        return validated_data


class TrackSerializer(serializers.Serializer):
    get_status_name = serializers.CharField(max_length=255)
