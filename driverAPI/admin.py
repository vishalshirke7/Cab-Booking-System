from django.contrib import admin

# Register your models here.
from .models import Driver, DriverLocation

admin.site.register(Driver)
admin.site.register(DriverLocation)