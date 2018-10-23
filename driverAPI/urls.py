from django.urls import path
from . import views

app_name = 'driverAPI'

urlpatterns = [

    path('register/', views.DriverRegistration.as_view(), name='driver-login'),
    path('login/', views.DriverLogin.as_view(), name='driver-login'),
    path('send_location/', views.GetDriverLocations.as_view(), name='driver-location')

]