from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils import timezone
    
class UserProfile(models.Model):
    def __str__(self):
        return self.fullname()
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
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
    def __str__(self):
        return self.p_name
    
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
    def __str__(self):
        return self.user.username
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessory = models.ForeignKey(MedicalAccessories, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_cost = models.IntegerField(null = True)
    
    
class Bill(models.Model):
    def __str__(self):
        return self.customer.username
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    accessory = models.ForeignKey(MedicalAccessories, on_delete=models.CASCADE)
    
    
class Doctor(models.Model): 
    def __str__(self):
        return self.name
    
    image = models.ImageField()
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    cost = models.IntegerField()
    available_spots = models.PositiveIntegerField()

class DoctorTimeSlot(models.Model):
    def __str__(self):
        return f"{self.doctor.name} ({self.start_time} - {self.end_time})"
  
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

class Appointment(models.Model):
    def __str__(self):
        return self.user.username
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    doctor_time_slot = models.ForeignKey(DoctorTimeSlot, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    appointment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Hospital(models.Model):
    hospital_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    blood_samples = models.ManyToManyField('Blood', related_name='hospitals')

    def __str__(self):
        return self.hospital_name

class Blood(models.Model):
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('AB+', 'AB+'),
        ('O+', 'O+'),
        ('A-', 'A-'),
        ('B-', 'B-'),
        ('AB-', 'AB-'),
        ('O-', 'O-'),
    )

    blood_group = models.CharField(max_length=20, choices=BLOOD_GROUP_CHOICES)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()

    def is_available(self):
        return self.quantity > 0

    def __str__(self):
        return f"{self.blood_group}"