# serializers.py

from rest_framework import serializers
from core.models import *  
import json 

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id', 'name', 'contact_number') 

class CustomerSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Customer 
        fields = ('id', 'name', 'contact_number') 

class ProductMaterialSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)

    class Meta:
        model = ProductMaterial
        fields = ('material', 'quantity', 'material_name')


class ProductSerializer(serializers.ModelSerializer):
    materials = ProductMaterialSerializer(many=True, required=False, write_only=True)
    material_details = serializers.SerializerMethodField(read_only=True) 
    # materials = serializers.SerializerMethodField(read_only=True) 

    class Meta:
        model = Product 
        fields = ('id', 'name', 'description', 'price', 'unit', 'materials', 'material_details')

    def get_materials(self, obj):
        return [material.name for material in obj.materials.all()]

    def get_material_details(self, obj):
        return [{'material': pm.material.name, 'quantity': pm.quantity} for pm in obj.product_materials.all()]

    def create(self, validated_data): 
        print(validated_data)
        materials_data = validated_data.pop('materials', []) 
        product = Product.objects.create(**validated_data) 
        print(materials_data) 
        for material_data in materials_data:
            ProductMaterial.objects.create(product=product, **material_data)
        return product

    def update(self, instance, validated_data):
        materials_data = validated_data.pop('materials', [])
        instance = super().update(instance, validated_data)

        instance.product_materials.all().delete()
        for material_data in materials_data:
            ProductMaterial.objects.create(product=instance, **material_data)
        return instance
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']     


class MaterialSerializer(serializers.ModelSerializer): 
    supplier = serializers.SerializerMethodField() 

    def get_supplier(self, material): 
        return material.supplier.name 

    class Meta:
        model = Material
        fields = ('id', 'name', 'price', 'unit', 'supplier')

class PurchaseMaterialSerializer(serializers.Serializer):
    material = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all())
    quantity = serializers.IntegerField()
    # material_name = serializers.CharField(source='material.name', read_only=True) 
    
class PurchaseSerializer(serializers.ModelSerializer):
    materials = PurchaseMaterialSerializer(many=True, required=False, write_only=True)
    material_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Purchase
        fields = ('id', 'supplier', 'materials', 'material_details')

    def get_material_details(self, obj):
        return [{'material': pm.material.name, 'quantity': pm.quantity} for pm in obj.purchasematerial_set.all()]

    def create(self, validated_data):
        materials_data = validated_data.pop('materials', [])
        purchase = Purchase.objects.create(**validated_data)
        for material_data in materials_data:
            PurchaseMaterial.objects.create(purchase=purchase, **material_data)
        return purchase

    def update(self, instance, validated_data):
        materials_data = validated_data.pop('materials', [])
        instance = super().update(instance, validated_data)

        instance.purchasematerial_set.all().delete()
        for material_data in materials_data:
            PurchaseMaterial.objects.create(purchase=instance, **material_data)
        return instance

class OrderProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity') 

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, required=False, write_only=True)
    product_names = serializers.SerializerMethodField(read_only=True)
    # order_products = OrderProductSerializer(many=True, read_only=True)

    def get_product_names(self, order): 
        qs = OrderProduct.objects.all().filter(order=order) 
        return [{'name': obj.product.name, 'quantity': obj.quantity} for obj in qs] 

    class Meta:
        model = Order
        fields = ('id', 'customer', 'products', 'order_status', 'product_names')

    def create(self, validated_data):
        products_data = validated_data.pop('products', []) 
        order = Order.objects.create(**validated_data)

        for item in products_data: 
            OrderProduct.objects.create(order=order, product=item['product'], quantity=item.get('quantity', 1))  # Default quantity to 1

        return order

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', [])
        instance = super().update(instance, validated_data)

        # Clear and repopulate related OrderProducts
        instance.order_products.all().delete()
        for product_id in products_data:
            OrderProduct.objects.create(order=instance, product_id=product_id, quantity=1)  # Default quantity to 1

        return instance

class StockSerializer(serializers.ModelSerializer):  
    material = serializers.SerializerMethodField() 

    def get_material(self, stock): 
        return stock.material.name 

    class Meta: 
        model = Stock 
        fields = ('material', 'quantity') 