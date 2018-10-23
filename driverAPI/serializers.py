from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Driver, DriverLocation, DriverRidesHistory
from passengerAPI.models import Passenger


class DriverRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class DriverLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email and password:
            raise ValidationError("Username and Password is required")
        try:
            driver = Driver.objects.get(email=email)
        except Driver.DoesNotExist:
            raise ValidationError("This email address does not exist")
        if driver.password == password:
            data["driver_id"] = driver.id
            return data
        else:
            raise ValidationError("Invalid credentials")


class DriverLocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        model = DriverLocation
        fields = '__all__'

    def create(self, validated_data):
        driver_id = self.context.get("driver_id")
        driver = Driver.objects.get(pk=driver_id)
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        obj = DriverLocation()
        obj.driver_id = driver
        obj.latitude = lat
        obj.longitude = lon
        obj.save()
        return obj



class PassengerTravelHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverRidesHistory
        fields = ['source_address',
                  'destination_address',
                  'car_no',
                  'booked_time',
                  'passenger_name']


class DriverInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['first_name',
                  'last_name',
                  'number',
                  'car_no'
                  ]



