import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from auth_app.models import UserOTP

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.SlugRelatedField(queryset=User.objects.filter(active=True), slug_field='phone_number')
    otp = serializers.SlugRelatedField(queryset=UserOTP.objects.all(), slug_field='otp')

    def validate_otp(self, data):
        time = datetime.datetime.now() - datetime.timedelta(minutes=5)
        user_otp = UserOTP.objects.filter(Q(otp=data.otp) & Q(date_created__gte=time))
        if not user_otp.exists():
            raise ValidationError("Please provide a valid OTP.")
        return data

    def validate_phone_number(self, data):
        user = User.objects.filter(Q(phone_number=data.phone_number) & Q(active=True))
        if not user.exists():
            raise ValidationError("Invalid information.")
        return data

    def validate(self, attrs):
        phone_number = attrs['phone_number']
        otp = attrs['otp']
        if otp.phone_number.phone_number != phone_number.phone_number:
            raise ValidationError("Invalid data.")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    extra_kwargs = {
        'password': {'write_only': True, 'read_only': True}
    }

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'phone_number',
            'password',
            'image',
        )

    def validate_phone_number(self, data):
        if User.objects.filter(phone_number=data).count() > 0:
            raise ValidationError("User is already exist.")
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            return user


class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, min_length=11)
    otp = serializers.CharField(max_length=6, required=False)

    def validate_phone_number(self, value):
        all_otp = UserOTP.objects.filter(phone_number=value, date_created__date=datetime.date.today())
        if all_otp.count() > 10:
            raise ValidationError("You have request maximum times for otp.")
        time = datetime.datetime.now() - datetime.timedelta(minutes=5)
        if all_otp.filter(date_created__gte=time).exists():
            raise ValidationError(
                "Please hold 5 min to get another code again. Maximum 10 code is available for a user per day.")
        return value


    def create(self, validated_data):
        user,_ = User.objects.get_or_create(phone_number = validated_data['phone_number'],defaults={'active': True})
        user = UserOTP.objects.create(phone_number=user)
        return user
