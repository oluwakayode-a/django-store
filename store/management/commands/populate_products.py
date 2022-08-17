import random
from django.core.management import BaseCommand
from store.models import Product, ProductCategory

from faker import Faker
import faker_commerce


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        faker.add_provider(faker_commerce.Provider)
        category = ProductCategory.objects.get(id=1)

        for i in range(30):
            product = Product.objects.create(
                name=faker.ecommerce_name(),
                description=faker.text(100),
                category=category,
                image=faker.image_url(),
                number_in_inventory=random.randint(1, 10),
                price=random.randrange(10, 100)
            )
            product.save()

            self.stdout.write(self.style.HTTP_INFO(f'Generated Product {product.name}'))
        
        self.stdout.write(self.style.SUCCESS('Done'))