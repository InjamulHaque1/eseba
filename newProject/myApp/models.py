from django.db import models

class User(models.Model):
    u_name = models.CharField(max_length=100)
    u_password = models.CharField(max_length=100)
    u_age = models.CharField(max_length=3)
    u_email = models.EmailField(unique=True)
    u_address = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    u_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    u_mobile = models.CharField(max_length=100, unique=True)
    
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