from django.db import models 
from  django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model 
import uuid 

class TimeStampedModel(models.Model): 
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True) 
    class Meta:
        abstract = True 

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        abstract = True  

class CreatedUpdatedBy(models.Model): 
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_%(class)s')  
    updated_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_%(class)s') 
    class Meta:
        abstract = True  

class ArchivedModel(models.Model): 
    is_archived = models.BooleanField(default=False) 
    class Meta:
        abstract = True 

class BaseModel(TimeStampedModel, UUIDModel, CreatedUpdatedBy, ArchivedModel):
    class Meta:
        abstract = True 

class User(AbstractUser, BaseModel):
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('user', 'User')], default='admin') 
    def __str__(self):
        return self.username   
    
class Supplier(BaseModel):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)   

    def __str__(self): 
        return self.name 

class Customer(BaseModel):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)  

    def __str__(self): 
        return self.name 

class Material(BaseModel): 
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    unit = models.CharField(max_length=10) 
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE) 

    def __str__(self): 
        return self.name 
    
class Product(BaseModel):
    name = models.CharField(max_length=100) 
    description = models.TextField(null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    unit = models.CharField(max_length=10, null=True) 
    materials = models.ManyToManyField(Material, through='ProductMaterial', related_name='products')

    def __str__(self):
        return self.name  
    
class ProductMaterial(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='product_materials')
    quantity = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self): 
        return f"{self.product.name} - {self.material.name}:{self.quantity}"  
    
class Stock(BaseModel):
    material = models.ForeignKey(Material, on_delete=models.CASCADE) 
    quantity = models.IntegerField(default=0) 

    def __str__(self):
        return f"{self.material.name}-{self.quantity}" 
    
class Purchase(BaseModel): 
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE) 
    materials = models.ManyToManyField(Material, through='PurchaseMaterial') 
    
    def __str__(self): 
        return self.supplier

class PurchaseMaterial(BaseModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0) 


    def __str__(self): 
        return f"{self.purchase.id} - {self.material.name}:{self.quantity}" 

class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct') 
    order_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending') 
    def __str__(self):
        return f"{self.customer.name} - {self.order_status}"

class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products') 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products') 
    quantity = models.IntegerField(default=0) 
    def __str__(self):
        return f"{self.order.id} - {self.product.name}:{self.quantity}" 


class MaterialConsumption(BaseModel): 
    order_product_id = models.ForeignKey(OrderProduct, on_delete=models.CASCADE, related_name='materials_consumed') 
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='materials_consumed') 
    quantity = models.IntegerField(default=0) 
    is_allocated = models.BooleanField(default=False) 
    def __str__(self):
        return f"{self.order_product_id.order.id} - {self.material_id.name}:{self.quantity}"

