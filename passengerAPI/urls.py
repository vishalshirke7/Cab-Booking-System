from django.urls import path
from . import views

app_name = 'passengerAPI'

urlpatterns = [

    path('register/', views.PassengerRegistration.as_view(), name='passenger-registration'),
    path('login/', views.PassengerLogin.as_view(), name='passenger-login'),
    path('logout/', views.Logout.as_view(), name='passenger-logout'),
    path('available_cabs/', views.GetListOfAvailableCab.as_view(), name='getlistofavailablecabs'),
    path('bookcab/', views.BookCab.as_view(), name='bookcab'),
    path('travelhistory/', views.TravelHistoryList.as_view(), name='travelhistory')

]