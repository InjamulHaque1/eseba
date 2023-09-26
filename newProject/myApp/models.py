from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER)

    def __str__(self):
        return self.user.username   

@receiver(post_delete, sender=UserProfile)
def delete_user_profile(sender, obj, **kwargs):
    try:
        obj.user.delete()
    except User.DoesNotExist:
        pass

class MedicalAccessories(models.Model):
    p_image = models.ImageField()
    p_name = models.CharField(max_length=100)
    p_description = models.CharField(max_length=1000)
    CATEGORY = (
        ('Medicine', 'Medicine'),
        ('Equipment', 'Equipment'),
    )
    p_category = models.CharField(max_length=10, choices=CATEGORY)
    p_cost = models.IntegerField()
    p_count = models.IntegerField()
    v_name = models.CharField(max_length=100)
    v_description = models.CharField(max_length=100)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessory = models.ForeignKey(MedicalAccessories, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_cost = models.IntegerField(null = True)
    
    