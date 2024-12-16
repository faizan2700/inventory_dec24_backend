from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Supplier, Product, Material, ProductMaterial 

class ProductAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up data for all tests."""   
        

        cls.supplier = Supplier.objects.create(name="Test Supplier", contact_number="1234567890")
        cls.material1 = Material.objects.create(name="Material 1", price=10, supplier = cls.supplier)  
        cls.material2 = Material.objects.create(name="Material 2", price=10, supplier = cls.supplier) 

    def test_product_creation(self): 
        url = 'http://127.0.0.1:8000/api/products/' 
        id1 = self.material1.id 
        id2 = self.material2.id 
        print(id1, id2) 
        data = {
            "name": "Test Product", 
            "description": "This is a test product.", 
            "price": 100.0,
            "unit": "kg", 
            "materials": [
                {"material": str(id1), "quantity": 10},
                {"material": str(id2), "quantity": 5}
            ]
        } 

        import json 

        response = self.client.post(url, data=data, format='json') 
        print(response.content) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 


    # def test_product_list_get(self):
    #     """Test GET request to list all products."""
    #     url = reverse('product-list')  # Adjust with your correct URL name
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertGreater(len(response.data), 0, "No products found in the response")

    # def test_product_create_post(self):
    #     """Test POST request to create a new product."""
    #     url = reverse('product-list')  # Adjust with your correct URL name
    #     data = {
    #         "name": "New Product",
    #         "price": 150.0,
    #         "quantity": 30,
    #         "supplier": str(self.supplier.id)
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['name'], "New Product")

    # def test_product_detail_get(self):
    #     """Test GET request to retrieve a product detail."""
    #     url = reverse('product-detail', kwargs={'pk': self.product.id})  # Adjust with your correct URL name
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name'], self.product.name)

    # def test_product_update_put(self):
    #     """Test PUT request to update an existing product."""
    #     url = reverse('product-detail', kwargs={'pk': self.product.id})  # Adjust with your correct URL name
    #     data = {
    #         "name": "Updated Product",
    #         "price": 120.0,
    #         "quantity": 60,
    #         "supplier": str(self.supplier.id)
    #     }
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name'], "Updated Product")

    # def test_product_partial_update_patch(self):
    #     """Test PATCH request to partially update an existing product."""
    #     url = reverse('product-detail', kwargs={'pk': self.product.id})  # Adjust with your correct URL name
    #     data = {"price": 200.0}
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['price'], 200.0)

    # def test_product_delete(self):
    #     """Test DELETE request to delete a product."""
    #     url = reverse('product-detail', kwargs={'pk': self.product.id})  # Adjust with your correct URL name
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     # Confirm that the product is deleted
    #     product_exists = Product.objects.filter(id=self.product.id).exists()
    #     self.assertFalse(product_exists, "Product was not deleted")
