import random

from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed

from basic_module_app.models import Brand, ProductType, Category, Collection

seeder = Seed.seeder()

from product_app.models import Product, ProductImage


class Command(BaseCommand):
    help = 'Fake seeder for products'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        seeder.add_entity(Product, 10, {
            'name': lambda x: seeder.faker.name(),
            'sku': lambda x: seeder.faker.name(),
            'quantity': lambda x: random.randint(0, 1000),
            'product_price': lambda x: random.randint(100, 10000),
            'selling_price': lambda x: random.randint(100, 10000),
            'offer_price': lambda x: random.randint(0, 100),
            'offer_start': lambda x: seeder.faker.date_time_this_year(),
            'offer_end': lambda x: seeder.faker.date_time_this_year(),
            'next_stock_date': lambda x: seeder.faker.date_time_this_year(),
            'description': lambda x: seeder.faker.sentence(),
            'brand': lambda x: Brand.objects.get(id=random.randint(4, 7)),
            'type': lambda x: ProductType.objects.get(id=random.randint(2, 4)),
            # 'categories': lambda x: random.randint(5, 7),
            # 'collections': lambda x: Collection.objects.get(id=random.randint(5, 6)),
        })
        seeder.add_entity(ProductImage, 20, {
            'product': lambda x: Product.objects.last(),
            'image': lambda x: seeder.faker.image_url(),

        })
        inserted_pks = seeder.execute()
