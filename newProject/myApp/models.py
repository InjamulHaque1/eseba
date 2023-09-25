from django.db import models

from django.db import models
from django.contrib.auth.models import User
    
class MedicalAccessories(models.Model):
    p_image = models.ImageField()
    p_name = models.CharField(max_length=100)
    p_description = models.CharField(max_length=100)
    CATEGORY = (
        ('Medicine', 'Medicine'),
        ('Equipment', 'Equipment'),
    )
    p_category = models.CharField(max_length=10, choices=CATEGORY)
    p_cost = models.IntegerField()
    p_count = models.IntegerField()
    v_name = models.CharField(max_length=100)
    v_description = models.CharField(max_length=100)

class Buys(models.Model):
    quantity = models.IntegerField()
    totalCost = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accessories_bought')
    accessory = models.ForeignKey(MedicalAccessories, on_delete=models.CASCADE, related_name='buyers')
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessory = models.ForeignKey(MedicalAccessories, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)