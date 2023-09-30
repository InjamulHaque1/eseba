from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils import timezone
    
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

@receiver(pre_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    try:
        profile = UserProfile.objects.get(user=instance)
        profile.delete()
    except UserProfile.DoesNotExist:
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
    
class Bill(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    accessory = models.ForeignKey(MedicalAccessories, on_delete=models.CASCADE)
    
class Doctor(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    cost = models.IntegerField()
    day_slots = models.CharField(max_length=255)
    time_slots = models.CharField(max_length=255)
    available_spots = models.PositiveIntegerField()

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    appointment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)