import decimal

from django.shortcuts import render, HttpResponse, redirect, reverse
from rest_framework import viewsets, views, generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from driverAPI.models import DriverLocation
from driverAPI.serializers import DriverInfoSerializer
from .models import Passenger, TravelHistory
from rest_framework import serializers
from .serializers import PassengerRegistrationSerializer, PassengerLoginSerializer, GetAvailableCabSerializer, BookCabSerializer, PassengerTravelHistorySerializer
from django.contrib.auth import login

import geopy.distance
import googlemaps
import requests


# gmaps = googlemaps.Client(key='AIzaSyAmQMbreF-nBNB3T527hAxyXZ9-KsUj-sU')


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
            gmaps = googlemaps.Client(key='AIzaSyA6vUErWEUlI8co4Qj5k4M6C3Efg5Wp6wY')
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
                print("Passenger ID ----------------->> %s" % request.session['passenger_id'])
                return Response(serializer.data)
            else:
                data = {"Unavailable": "Sorry, no cabs are available at this time"}
                print("Passenger ID ----------------->> %s" % request.session['passenger_id'])
                return Response(data)
            # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCab(APIView):

    serializer_class = BookCabSerializer

    def post(self, request, format=None):
        context = {
            'passenger_id': request.session['passenger_id'],
            'source_address': request.session['source_address'],
            'destination_address': request.session['destination_address']
            }
        print(request.session['passenger_id'])
        print(request.session['source_address'])
        print(request.session['destination_address'])
        serializer = BookCabSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            print("Passenger ID ----------------->> %s" % request.session['passenger_id'])
            data = {
                "Success": "Cab booked successfully"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TravelHistoryList(APIView):

    serializer_class = PassengerTravelHistorySerializer

    def get(self, request, format=None):
        passenger_id = request.session['passenger_id']
        print("Passenageyu iioioa voh uv oa v aiov ha   %s"%passenger_id)
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

