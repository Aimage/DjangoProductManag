from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import Product, Category
from ..serializers import ProductSerializer

class ProductTestView(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.product_id = 0
        self.product_data = {"name": 'product1',
                              "code": "789DF12",
                              "price": 14.2,
                              "quantity": 10,
                            }
        self.prod1 = Product.objects.create(
            name='prod1', code='1234', price=12.4, quantity=10)

        self.categ1 = Category.objects.create(name='category1')
        self.categ2 = Category.objects.create(name='category2')

    def test_create_product(self):
        response = self.client.post(reverse('api:product-list'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.product_data["name"])
        self.assertEqual(response.data["price"], self.product_data["price"])
        
    def test_get_products(self):
        response = self.client.get(reverse('api:product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_product_detail(self):
        response = self.client.get(reverse('api:product-detail', kwargs={'pk':self.prod1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_add_product_to_category(self):
        response = self.client.get(reverse('api:product-detail', kwargs={'pk':self.prod1.id}))
        data = response.data
        data["category"] = [self.categ1.id]
        response =  self.client.put(reverse('api:product-detail', kwargs={'pk':self.prod1.id}), data, format='json')
        self.assertEqual(response.data["category"], [self.categ1.id])

    def test_add_product_to_multiple_category(self):
        response = self.client.get(reverse('api:product-detail', kwargs={'pk':self.prod1.id}))
        data = response.data
        data["category"] = [self.categ1.id, self.categ2.id]
        response =  self.client.put(reverse('api:product-detail', kwargs={'pk':self.prod1.id}), data, format='json')
        self.assertEqual(response.data["category"], [self.categ1.id, self.categ2.id])
        
    def test_delete_product(self):
        response = self.client.delete(reverse('api:product-detail', kwargs={'pk':self.prod1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse('api:product-detail', kwargs={'pk':self.prod1.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class CategoryTestView(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.category_data = {"name": 'categ1',
                              "parent_category": None,
                              "product_id": []
                            }
        
        self.prod1 = Product.objects.create(
            name='prod1', code='1234', price=12.4, quantity=10)
        self.prod2 = Product.objects.create(
            name='prod2', code='5678', price=2.4, quantity=20)

        self.categ1 = Category.objects.create(name='category1')
        self.categ2 = Category.objects.create(name='category2')
        
        self.categ3 = Category.objects.create(name='category3')
        self.categ3.product_id.add(self.prod1)
        self.categ3.product_id.add(self.prod2)
        
    def test_create_category(self):
        response = self.client.post(reverse('api:category-list'), self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.category_data["name"])
        
    def test_get_categorys(self):
        response = self.client.get(reverse('api:category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_gategory(self):
        response = self.client.get(reverse('api:category-detail', kwargs={'pk':self.categ1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_add_child_category_to_category(self):
        """Put category2 as subcategory of category1 to form a tree"""
        
        response = self.client.get(reverse('api:category-detail', kwargs={'pk':self.categ2.id}))
        data = response.data 
        data["parent_category"] = self.categ1.id
        response = self.client.put(reverse('api:category-detail', kwargs={'pk':self.categ2.id}), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["parent_category"], self.categ1.id)
        
    def test_add_product_to_category(self):
        response = self.client.get(reverse('api:category-detail', kwargs={'pk':self.categ1.id}))
        data = response.data 
        data["product_id"].append(self.prod1.id)
        response = self.client.put(reverse('api:category-detail', kwargs={'pk':self.categ1.id}), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.prod1.id, response.data["product_id"])
        
    def test_add_multiple_product_to_category(self):
        response = self.client.get(reverse('api:category-detail', kwargs={'pk':self.categ1.id}))
        data = response.data 
        data["product_id"].append(self.prod1.id)
        data["product_id"].append(self.prod2.id)
        response = self.client.put(reverse('api:category-detail', kwargs={'pk':self.categ1.id}), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.prod1.id, response.data["product_id"])
        self.assertIn(self.prod2.id, response.data["product_id"])
        
    def test_delete_category(self):
        """ delete category and verify if corresponding products are not deleted """
        response = self.client.get(reverse('api:category-detail', kwargs={'pk':self.categ3.id}))
        self.assertIn(self.prod1.id, response.data["product_id"])        
        self.assertIn(self.prod2.id, response.data["product_id"])        
        
        response = self.client.delete(reverse('api:category-detail', kwargs={'pk':self.categ3.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse('api:category-detail', kwargs={'pk':self.categ3.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        response = self.client.get(reverse('api:product-detail', kwargs={'pk':self.prod1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('api:product-detail', kwargs={'pk':self.prod2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        