from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(CartItem)
admin.site.register(MedicalAccessories)
admin.site.register(Bill)
admin.site.register(BillItem)
admin.site.register(Doctor) 
admin.site.register(DoctorTimeSlot) 
admin.site.register(Appointment)
admin.site.register(Hospital)
admin.site.register(Blood)