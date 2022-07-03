import json

import ujson
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from basic_module_app.models import Category, Variation, Collection, Brand, ProductType, Coupon
from custom_admin_app.forms import ProductCreateBasicForm
from product_app.models import Product, ProductImage, ProductVariation, ProductVariationValues
from product_app.serializers import ProductVariationSerializer


class IndexPage(TemplateView):
    template_name = 'index.html'


class CategoryIndex(ListView):
    template_name = 'category/index.html'
    queryset = Category.objects.all()
    context_object_name = 'categories'


class VariationIndex(ListView):
    template_name = 'variation/index.html'
    queryset = Variation.objects.all()


class CollectionIndex(ListView):
    template_name = 'collection/index.html'
    queryset = Collection.objects.all()


class BrandIndex(ListView):
    template_name = 'brand/index.html'
    queryset = Brand.objects.all()


class TypeIndex(ListView):
    template_name = 'product_type/index.html'
    queryset = ProductType.objects.all()


class CouponIndex(ListView):
    template_name = 'coupon/index.html'
    queryset = Coupon.objects.all()


class CategoryCreate(CreateView):
    template_name = 'category/edit.html'
    model = Category
    fields = ['name', 'parent', 'trash']
    success_url = reverse_lazy("main:category.index")
    # context_object_name = 'category'


class VariationCreate(CreateView):
    template_name = 'variation/edit.html'
    model = Variation
    fields = ['name', 'trash']
    success_url = reverse_lazy("main:variation.index")


class BrandCreate(CreateView):
    template_name = 'brand/edit.html'
    model = Brand
    fields = ['name', 'trash']
    success_url = reverse_lazy("main:brand.index")


class CollectionCreate(CreateView):
    template_name = 'collection/edit.html'
    model = Collection
    fields = ['name', 'trash']
    success_url = reverse_lazy("main:collection.index")


class TypeCreate(CreateView):
    template_name = 'product_type/edit.html'
    model = ProductType
    fields = ['name', 'trash']
    success_url = reverse_lazy("main:type.index")


class CouponCreate(CreateView):
    template_name = 'coupon/edit.html'
    model = Coupon
    fields = ['name', 'reduce_money', 'trash']
    success_url = reverse_lazy("main:coupon.index")


class CategoryUpdate(UpdateView):
    template_name = 'category/edit.html'
    model = Category
    fields = ['name', 'parent', 'trash']
    success_url = reverse_lazy("main:category.index")
    # context_object_name = 'category'


class VariationUpdate(UpdateView):
    template_name = 'variation/edit.html'
    model = Variation
    fields = ['name', 'trash']
    success_url = reverse_lazy("main:variation.index")
    # context_object_name = 'category'


class CollectionUpdate(UpdateView):
    template_name = 'collection/edit.html'
    model = Collection
    fields = ['name', 'trash']
    success_url = reverse_lazy("main:collection.index")
    # context_object_name = 'category'


class BrandUpdate(UpdateView):
    template_name = 'brand/edit.html'
    model = Brand
    fields = ['name', 'trash']
    success_url = reverse_lazy("main:brand.index")


class TypeUpdate(UpdateView):
    template_name = 'product_type/edit.html'
    model = ProductType
    fields = ['name', 'trash']
    success_url = reverse_lazy("main:type.index")


class CouponUpdate(UpdateView):
    template_name = 'coupon/edit.html'
    model = Coupon
    fields = ['name', 'reduce_money', 'trash']
    success_url = reverse_lazy("main:coupon.index")


class CategoryDelete(DeleteView):
    model = Category
    template_name = 'category/delete.html'
    success_url = reverse_lazy('main:category.index')


class VariationDelete(DeleteView):
    model = Variation
    template_name = 'variation/delete.html'
    success_url = reverse_lazy('main:variation.index')


class CollectionDelete(DeleteView):
    model = Collection
    template_name = 'collection/delete.html'
    success_url = reverse_lazy('main:collection.index')


class BrandDelete(DeleteView):
    model = Brand
    template_name = 'brand/delete.html'
    success_url = reverse_lazy('main:brand.index')


class TypeDelete(DeleteView):
    model = ProductType
    template_name = 'product_type/delete.html'
    success_url = reverse_lazy('main:type.index')


class CouponDelete(DeleteView):
    model = Coupon
    template_name = 'coupon/delete.html'
    success_url = reverse_lazy('main:coupon.index')


class ProductIndex(ListView):
    # model = Product
    template_name = 'product/index.html'
    queryset = Product.objects.prefetch_related(
        "get_product_cart_products__variation__get_product_variation_values", "categories", "brand", "type",
        "collections", Prefetch('get_product_images', queryset=ProductImage.objects.filter(primary=True))).all()


class ProductCreate(CreateView):
    template_name = 'product/create/basic.html'
    form_class = ProductCreateBasicForm

    def post(self, request, *args, **kwargs):
        form = ProductCreateBasicForm(request.POST)
        if form.is_valid():
            instance = form.save()

            return redirect(reverse_lazy("main:product.create.variance", kwargs={'pk': instance.id}))
        return render(request, self.template_name, {'form': form})


class ProductVarianceCreate(View):
    template_name = 'product/create/variation.html'

    def get(self, request, **kwargs):
        context = {"product": Product.objects.get(id=kwargs['pk'])}
        return render(request, self.template_name, context=context)
    # def get_context_data(self, **kwargs):
    #     context = super(ProductVarianceCreate, self).get_context_data(**kwargs)
    #     context["product"] = Product.objects.get(id=context['pk'])
    #     return context

    # form_class = ProductCreateVarianceForm

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         instance = form.save(commit=False)
    #         request.session[f'product_create_{instance.id}'] = instance
    #         return
    #         # model = Product


class ProductVarianceCreateSave(CreateAPIView):
    serializer_class = ProductVariationSerializer

    def post(self, request, *args, **kwargs):
        basics = ujson.loads(request.data.getlist('data')[0])
        images = request.data.getlist('image')
        with transaction.atomic():
            for index, data in enumerate(basics):
                print(data)
                print("\n")
                product = Product.objects.get(id=data['product_id'])
                if product:
                    sku = data['sku']
                    quantity = data['quantity']
                    original_price = data['original_price']
                    offer_price = data['offer_price']
                    offer_start = data['offer_start']
                    offer_end = data['offer_end']
                    next_stock_date = data['next_stock_date']
                    # init variation model for saving
                    variation = ProductVariation()
                    variation.product = product
                    variation.sku = sku
                    variation.quantity = quantity
                    variation.original_price = original_price
                    variation.offer_price = offer_price
                    variation.offer_start = offer_start
                    variation.offer_end = offer_end
                    variation.next_stock_date = next_stock_date
                    variation.image = images[index]
                    variation.save()
                    # print('valus are: ', data['get_product_variation_values'])
                    # print('valus type: ', type(data['get_product_variation_values']))
                    for value in basics[index]['get_product_variation_values']:
                        print('value is ', value['variation'])
                        variation_model = Variation.objects.get(id=value["variation"])
                        print(f'model is {variation_model}')
                        print("variation: ", variation_model)
                        if variation_model and value['title']:
                            ProductVariationValues.objects.create(
                                product_variation=variation,
                                title=value['title'],
                                variation=variation_model
                            )
                        else:
                            raise ValueError(f"{variation.sku}\'s title or variation model is not available.  ")
                else:
                    raise ValueError(f"Product cannot found...")
                    # print(image)
        return Response(status=status.HTTP_200_OK)


class ProductImageCreate(View):
    def get(self, request, **kwargs):
        context = {"product": Product.objects.get(id=kwargs['pk'])}
        return render(request, 'product/create/image.html', context=context)

    def post(self, request, **kwargs):
        files = request.FILES.getlist("images")
        product = Product.objects.get(id=kwargs['pk'])
        for i in files:
            ProductImage.objects.create(product=product, image=i)
        product.active = True
        product.save()
        return redirect(reverse_lazy('main:product.index'))
