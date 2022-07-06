import datetime
import sys
import uuid
from io import StringIO, BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import get_default_timezone
from mptt.fields import TreeForeignKey

from EcommerceClient.mixins import CUMixin, get_file_path

User = get_user_model()


class BasicSetting(CUMixin):
    delivery_charge = models.DecimalField(max_digits=100, decimal_places=2, default=0)


class Category(CUMixin):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_file_path, max_length=500)
    slug = models.SlugField(null=True, blank=True, editable=False)
    directory_string_var = 'category'

    def __str__(self):
        return self.name


class Banner(CUMixin):
    text = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=get_file_path, max_length=500)
    link = models.CharField(null=True, blank=True, max_length=255)
    directory_string_var = 'banner'

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         imageTemproary = Image.open(self.image)
    #         outputIoStream = BytesIO()
    #         imageTemproaryResized = imageTemproary.resize((871, 313))
    #         imageTemproaryResized.save(outputIoStream, format='JPEG', quality=80)
    #         outputIoStream.seek(0)
    #         self.image = InMemoryUploadedFile(outputIoStream, 'ImageField',
    #                                           "%s.jpg" % uuid.uuid4(), 'image/jpeg',
    #                                           sys.getsizeof(outputIoStream), None)
    #     super(Banner, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Division(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class District(models.Model):
    division = models.ForeignKey(Division, related_name="get_districts", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PostOffice(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name="get_division_post_offices")
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="get_district_post_offices")
    name = models.CharField(max_length=255)
    code = models.PositiveIntegerField()

    def __str__(self):
        return self.name


#
# class Category(MPTTModel):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(null=True, blank=True, editable=False)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
#     date_created = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     trash = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.name
#
#     class MPTTMeta:
#         order_insertion_by = ['name']
#
#     def get_absolute_url(self):
#         return reverse('items-by-category', args=[str(self.slug)])


class Variation(CUMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, editable=False)

    def __str__(self):
        return self.name


class Collection(CUMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, editable=False)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True, max_length=500)
    directory_string_var = 'collections'

    def __str__(self):
        return self.name


class Brand(CUMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, editable=False)

    def __str__(self):
        return self.name


class ProductType(CUMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, editable=False)

    def __str__(self):
        return self.name


class UserAddress(CUMixin):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='user_locations')
    area = models.CharField(max_length=150, null=True, blank=True)
    street = models.CharField(max_length=150, null=True, blank=True)
    house = models.CharField(max_length=150, null=True, blank=True)
    post_office = models.ForeignKey(PostOffice, on_delete=models.CASCADE, related_name="get_user_addresses")
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="get_user_address_district")
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name="get_user_address_division")

    def __str__(self):
        return f'Area: {self.area} - District: {self.district.name} - Division: {self.division.name}'

    @property
    def full_address(self):
        return f'House: {self.house} - Street: {self.street} - Area: {self.area} - Post office: {self.post_office.name} - District: {self.district.name} - Division: {self.division.name} '


class Coupon(CUMixin):
    name = models.CharField(max_length=255)
    price = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    reduce_money = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    free_delivery = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserCoupon(CUMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    coupon = models.ForeignKey(Coupon, related_name="get_user_coupons", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="get_user_coupons", on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    # payment = models.BooleanField(default=False)


#
# class CouponBank(CUMixin):
#     tran_id = models.OneToOneField(UserCoupon, related_name="get_user_coupon_payment", on_delete=models.CASCADE,
#                                    null=False,
#                                    blank=True, primary_key=True)
#     val_id = models.CharField(max_length=255)
#     card_no = models.CharField(max_length=255, null=True, blank=True)
#     status = models.CharField(max_length=255)
#     card_issuer = models.CharField(max_length=255, null=True, blank=True)
#     card_brand = models.CharField(max_length=255, null=True, blank=True)
#     card_sub_brand = models.CharField(max_length=255, null=True, blank=True)
#     card_issuer_country = models.CharField(max_length=255, null=True, blank=True)
#     card_issuer_country_code = models.CharField(max_length=255, null=True, blank=True)
#     risk_level = models.CharField(max_length=255, null=True, blank=True)
#     risk_title = models.CharField(max_length=255, null=True, blank=True)
#     store_id = models.CharField(max_length=255)
#     bank_tran_id = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
#     store_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
#     card_type = models.CharField(max_length=255)
#     tran_date = models.DateTimeField()
#     currency = models.CharField(max_length=255)
#     currency_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
#     currency_rate = models.DecimalField(max_digits=100, decimal_places=4, default=0)
#     base_fair = models.DecimalField(max_digits=100, decimal_places=4, default=0)


class DeliveryFreeArea(models.Model):
    post_office = models.OneToOneField(PostOffice, related_name="get_free_delivery_areas",
                                       on_delete=models.CASCADE)

    def __str__(self):
        return self.post_office.name
