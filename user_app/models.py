import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from django.db.models import Sum

from EcommerceClient.mixins import CUMixin
from basic_module_app.models import Coupon, UserAddress
from product_app.models import Product, ProductVariation

User = get_user_model()


class Cart(CUMixin):
    user = models.ForeignKey(User, related_name="get_user_carts", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    @property
    def total_price(self) -> Decimal:
        if self.get_cart_products.count() > 0:
            cart_products = self.get_cart_products.all()
            total_price = Decimal(0)
            for product in cart_products:
                if product.variation:
                    selling_price = product.variation.selling_price
                else:
                    selling_price = product.product.selling_price
                if product.product.is_offer_valid:
                    selling_price -= product.product.offer_price
                total_price += (selling_price * product.quantity)
            return total_price
        else:
            return Decimal(0)

    @property
    def total_saving(self) -> Decimal:
        if self.get_cart_products.count() > 0:
            total = Decimal(0)
            cart_products = self.get_cart_products.all()
            for i in list(cart_products):
                total += i.total_saving_product
            return total


class CartProduct(CUMixin):
    cart = models.ForeignKey(Cart, related_name="get_cart_products", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="get_product_cart_products", on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, related_name="get_variation_cart_products",
                                  on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Please add 1 product to cart.")
        ],
    )

    @property
    def total_saving_product(self) -> Decimal:
        if self.product.is_offer_valid:
            return self.product.offer_price * self.quantity
        else:
            return Decimal(0)
            # return self.variation

    @property
    def final_price(self):
        if self.variation is not None:
            return self.variation.final_price
        else:
            return self.product.final_price

    @property
    def get_offer_price(self):
        if self.product.is_offer_valid:
            return self.product.offer_price
        else:
            return Decimal(0)


class Checkout(CUMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    status_choices = (
        (0, 'Payment Process'),
        (1, 'Order placed'),
        (2, 'Processing'),
        (3, 'Packaging'),
        (4, 'On-way'),
        (5, 'Reached'),
        (6, 'Completed'),
    )
    user = models.ForeignKey(User, related_name="get_user_checkout", on_delete=models.RESTRICT)
    cart = models.OneToOneField(Cart, related_name="get_cart_checkout", on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=100, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    save_money = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    coupon = models.ForeignKey(Coupon, related_name="get_coupon_checkouts", on_delete=models.CASCADE, null=True,
                               blank=True)
    address = models.ForeignKey(UserAddress, related_name="get_address_checkouts", on_delete=models.SET_NULL, null=True,
                                blank=True)
    order_status = models.PositiveSmallIntegerField(default=0, choices=status_choices)

    @property
    def get_status_name(self):
        return self.get_order_status_display()


class CheckoutPayment(CUMixin):
    tran_id = models.OneToOneField(Checkout, related_name="get_checkout_payment", on_delete=models.CASCADE, null=False,
                                   blank=True, primary_key=True)
    val_id = models.CharField(max_length=255)
    card_no = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255)
    card_issuer = models.CharField(max_length=255, null=True, blank=True)
    card_brand = models.CharField(max_length=255, null=True, blank=True)
    card_sub_brand = models.CharField(max_length=255, null=True, blank=True)
    card_issuer_country = models.CharField(max_length=255, null=True, blank=True)
    card_issuer_country_code = models.CharField(max_length=255, null=True, blank=True)
    risk_level = models.CharField(max_length=255, null=True, blank=True)
    risk_title = models.CharField(max_length=255, null=True, blank=True)
    store_id = models.CharField(max_length=255)
    bank_tran_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    store_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    card_type = models.CharField(max_length=255)
    tran_date = models.DateTimeField()
    currency = models.CharField(max_length=255)
    currency_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    currency_rate = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    base_fair = models.DecimalField(max_digits=100, decimal_places=4, default=0)


class CheckoutProduct(CUMixin):
    checkout = models.ForeignKey(Checkout, related_name="get_checkout_products", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="get_checkout_products", on_delete=models.SET_NULL, null=True,
                                blank=True)
    single_price = models.DecimalField(max_digits=100, decimal_places=2)
    offer_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Please add 1 product to checkout.")
        ]
    )
    variation = models.ForeignKey(ProductVariation, related_name="get_checkout_variations",
                                  on_delete=models.SET_NULL, null=True, blank=True)
