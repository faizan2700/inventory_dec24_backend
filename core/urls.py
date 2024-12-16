# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet) 
router.register(r'users', UserViewSet) 
router.register(r'suppliers', SupplierViewSet) 
router.register(r'customers', CustomerViewSet) 
router.register(r'materials', MaterialViewSet) 
router.register(r'purchases', PurchaseViewSet) 
router.register(r'orders', OrderViewSet)  
router.register(r'stocks', StockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
