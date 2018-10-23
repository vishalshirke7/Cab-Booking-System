from django.shortcuts import render, HttpResponse, redirect, reverse
from rest_framework import viewsets, views, generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from .models import Driver, DriverLocation
from .serializers import DriverRegistrationSerializer, DriverLocationSerializer, DriverLoginSerializer
from django.contrib.auth import login
import io
from rest_framework.parsers import JSONParser


class DriverRegistration(APIView):
    """
    Registering a Driver

    """
    serializer_class = DriverRegistrationSerializer

    def get(self, request, format=None):

        drivers = Driver.objects.all()
        serializer = DriverRegistrationSerializer(drivers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DriverRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverLogin(APIView):

    serializer_class = DriverLoginSerializer

    def post(self, request, format=None):
        serializer = DriverLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            request.session['driver_id'] = serializer.validated_data["driver_id"]
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDriverLocations(APIView):

    serializer_class = DriverLocationSerializer

    def get(self, request, format=None):
        driver_locations = DriverLocation.objects.all()
        serializer = DriverLocationSerializer(driver_locations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        driver_id = request.session['driver_id']
        context = {"driver_id": driver_id}
        serializer = DriverLocationSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

