from django.contrib.gis.geos import factory
from django.test import TestCase
from django.test.client import Client

from mainapp.models import Product, ProductCategory


# from django.core.management import call_command

class ProductCategoryFabric(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductCategory

    name = factory.Faker('name')


class ProductFabric(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(ProductCategoryFabric)
    name = factory.Faker('name')
    quantity = factory.Faker('random_int')
    price = factory.Faker('random_int')


class TestMainappSmoke(TestCase):
    def setUp(self):
        #        call_command('flush', '--noinput')
        #        call_command('loaddata', 'test_db.json')
        self.client = Client()
        categories = ProductCategoryFabric.create_batch(10)
        for category in categories:
            ProductFabric.create_batch(10, category=category)

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)

#    def tearDown(self):
#        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', \
#                     'basketapp')
