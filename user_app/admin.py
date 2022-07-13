from django.contrib import admin

# Register your models here.
from user_app.models import Cart, CartProduct, CheckoutProduct, Checkout


class CartProductAdmin(admin.TabularInline):
    model = CartProduct


class CheckoutProductAdmin(admin.TabularInline):
    model = CheckoutProduct


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartProductAdmin]
    model = Cart


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    inlines = [CheckoutProductAdmin]
    model = Checkout
    list_display = ['id']
