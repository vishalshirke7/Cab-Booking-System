from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from functools import partial

from .models import Driver, DriverLocation, DriverRidesHistory
from .serializers import DriverRegistrationSerializer
from .serializers import DriverLoginSerializer
from .serializers import DriverLocationSerializer, PassengerTravelHistorySerializer


class CustomPermissions(permissions.BasePermission):

    def __init__(self, allowed_methods):
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        if 'driver_id' in request.session.keys():
            return request.method in self.allowed_methods


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

    """
    Log in a driver

    """
    serializer_class = DriverLoginSerializer

    def post(self, request, format=None):
        serializer = DriverLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            request.session['driver_id'] = serializer.validated_data["driver_id"]
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDriverLocations(APIView):

    """
    This function gets the locations of all active drivers who are currently driving the cab

    """
    serializer_class = DriverLocationSerializer
    permission_classes = (partial(CustomPermissions, ['GET', 'HEAD', 'POST']),)

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


class DriverTravelHistoryList(APIView):

    serializer_class = PassengerTravelHistorySerializer
    permission_classes = (partial(CustomPermissions, ['GET', 'HEAD', 'POST']),)

    def get(self, request, format=None):
        driver_id = request.session['driver_id']
        driver = Driver.objects.get(pk=driver_id)
        travel_history = DriverRidesHistory.objects.filter(driver_id=driver)
        if len(travel_history) > 0:
            serializer = PassengerTravelHistorySerializer(travel_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {"No history": "You do not have any history of travelling"}
            return Response(data)


class Logout(APIView):

    def get(self, request, format=None):
        del request.session['driver_id']
        data = {"logout": "logged out successfully"}
        return Response(data, status=status.HTTP_200_OK)
