from django.shortcuts import render, HttpResponse, redirect, reverse
from rest_framework import viewsets, views, generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Passenger
from rest_framework import serializers
from .serializers import PassengerRegistrationSerializer, PassengerLoginSerializer, GetAvailableCabSerializer
from django.contrib.auth import login
from driverAPI.models import DriverLocation
import geopy.distance
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyCT1sx-7md2wnlJ0wGTj2TwucsEYCRV-4s')


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

    serializer_class = GetAvailableCabSerializer

    def post(self, request, format=None):
        serializer = GetAvailableCabSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # passenger_coords = (52.2296756, 21.0122287)
            # coords_2 = (52.406374, 16.9251681)
            geocode_result = gmaps.geocode(request.data['Destination_address'])
            abc = geocode_result[0][0][1][1]
            print("-------------------->>>> %s"%abc)
            data = {'lat_long': geocode_result}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
