from django.test import TestCase
from ..models import Product


class ProductTest(TestCase):
    """ Test module for Product model """

    def setUp(self):
        Product.objects.create(
            name='prod1', code='1234', price=12.4, quantity=10)
        Product.objects.create(
            name='prod2', code='4567', price=1.4, quantity=20)

    def test_product(self):
        prod1 = Product.objects.get(name='prod1')
        prod2 = Product.objects.get(name='prod2')
        self.assertEqual(
            prod1.price, 12.4)
        self.assertEqual(
            prod2.name, "prod2")