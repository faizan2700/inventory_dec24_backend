from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import *

@receiver(post_save, sender=Purchase)
def post_save_handler(sender, instance, created, **kwargs):
    if created:
        qs = PurchaseMaterial.objects.filter(purchase=instance) 
        for p_material in qs: 
            material_stock, _ = Stock.objects.get_or_create(material=p_material.material) 
            material_stock.quantity += p_material.quantity 
