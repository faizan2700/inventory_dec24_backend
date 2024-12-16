from rest_framework.viewsets import ModelViewSet
from .models import Supplier, Customer, User, Product, Material, Order, Purchase, Stock
from .serializers import (
    SupplierSerializer,
    CustomerSerializer,
    UserSerializer,
    ProductSerializer,
    MaterialSerializer,
    OrderSerializer,
    PurchaseSerializer, 
    StockSerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

class StockViewSet(ModelViewSet): 
    queryset = Stock.objects.all() 
    serializer_class = StockSerializer 



@api_view(['GET'])
def simple_api_view(request):
    return Response({
        'total_revenue': 100, 
        'number_of_orders': 200, 
        'best_selling_product': 'Smartphone', 
        'revenue_trends': 'Daily', 
        'inventory_value': '25000$', 
        'low_stock_alert': '5 Products', 
        'upcoming_releases': '2 digital products', 
        'revenue_distribution': '60% Physical', 
    })