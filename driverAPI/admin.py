from django.contrib import admin

# Register your models here.
from .models import Driver, DriverLocation, DriverRidesHistory

admin.site.register(Driver)
admin.site.register(DriverLocation)
admin.site.register(DriverRidesHistory)
# admin.site.register(DriverLocation)