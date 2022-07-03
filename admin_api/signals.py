from django.conf import settings
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from product_app.models import ProductImage

#
# @receiver(pre_delete, sender=ProductImage)
# def delete_product_image(sender, instance, *args, **kwargs):
#     imagekit_url = imagekit.url({
#         "path": instance.image,
#         "url_endpoint": settings.IMAGEKIT_ENDPOINT,
#     })
#
#     res = imagekit.delete_file(imagekit_url)
#     print(res)
#     if res['response'] is None:
#         raise ValidationError(res['error'])
