import decimal
from functools import partial
from rest_framework import viewsets, views, generics, status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from driverAPI.models import DriverLocation
from driverAPI.serializers import DriverInfoSerializer
from .models import Passenger, TravelHistory
from rest_framework import serializers
from .serializers import PassengerRegistrationSerializer, PassengerLoginSerializer, GetAvailableCabSerializer, BookCabSerializer, PassengerTravelHistorySerializer
import geopy.distance
import googlemaps
import requests


class CustomPermissionsForPassenger(permissions.BasePermission):

    def __init__(self, allowed_methods):
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        if 'passenger_id' in request.session.keys():
            return request.method in self.allowed_methods


class PassengerRegistration(APIView):
    """
    Register a Passenger

    """
    serializer_class = PassengerRegistrationSerializer

    def get(self, request, format=None):
        customers = Passenger.objects.all()
        serializer = PassengerRegistrationSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PassengerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassengerLogin(APIView):

    serializer_class = PassengerLoginSerializer

    def post(self, request, format=None):
        serializer = PassengerLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            request.session['passenger_id'] = serializer.validated_data["passenger_id"]
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetListOfAvailableCab(APIView):

    """
    This function returns a list of available drivers, according the source address given by passenger
    It uses geoencoding api of google maps to convert latitude, longitude to address and vice versa.
    Calculating available cabs is done by calculating distance between source address and available cabs location.
    If this distance is < 4 kms,  then these cabs are shown as available.

    """

    serializer_class = GetAvailableCabSerializer
    permission_classes = (partial(CustomPermissionsForPassenger, ['GET', 'HEAD', 'POST']),)

    def post(self, request, format=None):
        serializer = GetAvailableCabSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            gmaps = googlemaps.Client(key='AIzaSyALWKpmu1YBGDTS7waWGFdokZgYWYJIQtE')
            request.session['source_address'] = request.data['Source_address']
            request.session['destination_address'] = request.data['Destination_address']
            geocode_result = gmaps.geocode(request.data['Source_address'])
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lon = geocode_result[0]["geometry"]["location"]["lng"]

            driver_locations = DriverLocation.objects.all()
            available_drivers_list = []
            for location in driver_locations:
                coords_1 = (lat, lon)
                coords_2 = (location.latitude, location.longitude)
                distance = geopy.distance.vincenty(coords_1, coords_2).km
                if distance < 4:
                    driver = location.driver_id
                    available_drivers_list.append(driver)
            if available_drivers_list:
                serializer = DriverInfoSerializer(available_drivers_list, many=True)
                return Response(serializer.data)
            else:
                data = {"Unavailable": "Sorry, no cabs are available at this time"}
                return Response(data)
            # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCab(APIView):

    """
    This function makes a request to book cab by entering car_no, (selecting an available cab from map i.e tapping on it
    in real scenario) and arrange a ride.

    """
    serializer_class = BookCabSerializer
    permission_classes = (partial(CustomPermissionsForPassenger, ['GET', 'HEAD', 'POST']),)

    def post(self, request, format=None):
        context = {
            'passenger_id': request.session['passenger_id'],
            'source_address': request.session['source_address'],
            'destination_address': request.session['destination_address']
            }
        serializer = BookCabSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            data = {
                "Success": "Cab booked successfully"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TravelHistoryList(APIView):

    serializer_class = PassengerTravelHistorySerializer
    permission_classes = (partial(CustomPermissionsForPassenger, ['GET', 'HEAD', 'POST']),)

    def get(self, request, format=None):
        passenger_id = request.session['passenger_id']
        passenger = Passenger.objects.get(pk=passenger_id)
        travel_history = TravelHistory.objects.filter(passenger_id=passenger)
        if len(travel_history) > 0:
            serializer = PassengerTravelHistorySerializer(travel_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {"No history": "You do not have any history of travelling"}
            return Response(data)


class Logout(APIView):

    def get(self, request, format=None):
        del request.session['passenger_id']
        data = {'Logout': 'logged out successfully'}
        return Response(data, status=status.HTTP_200_OK)

