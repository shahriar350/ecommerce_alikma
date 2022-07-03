from django import forms
from django.forms import DateTimeInput, DateInput
from django_quill.forms import QuillFormField

from basic_module_app.models import Category, Variation, Collection, Brand, ProductType, UserDeliveryCharge, Coupon
from product_app.models import Product, ProductVariation, ProductVariationValues, ProductImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = "__all__"


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = "__all__"


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = "__all__"


class UserDeliveryChargeForm(forms.ModelForm):
    class Meta:
        model = UserDeliveryCharge
        fields = "__all__"


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"


class ProductVariationValuesForm(forms.ModelForm):
    class Meta:
        model = ProductVariationValues
        fields = (
            'id',
            'product_variation',
            'variation',
            'title',
        )


class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = (
            'id',
            'product',
            'sku',
            'quantity',
            'original_price',
            'offer_price',
            'offer_start',
            'offer_end',
            'next_stock_date',
            'image',
        )


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductCreateBasicForm(forms.ModelForm):
    description = QuillFormField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'sku',
            'quantity',
            'original_price',
            'offer_price',
            'offer_start',
            'offer_end',
            'next_stock_date',
            'description',
            'brand',
            'type',
            'categories',
            'collections',
        )

        widgets = {
            'offer_start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'offer_end': DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_stock_date': DateInput(attrs={'type': 'date'}),
        }



class ProductCreateVarianceForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = "__all__"

        widgets = {
            'offer_start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'offer_end': DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_stock_date': DateInput(attrs={'type': 'date'}),
        }
