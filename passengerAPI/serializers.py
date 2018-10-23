from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from driverAPI.models import Driver, DriverRidesHistory
from .models import Passenger, TravelHistory


class PassengerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'


class PassengerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email and password:
            raise ValidationError("Username and Password is required")
        try:
            passenger = Passenger.objects.get(email=email)
        except Passenger.DoesNotExist:
            raise ValidationError("This email address does not exist")
        if passenger.password == password:
            data["passenger_id"] = passenger.id
            return data
        else:
            raise ValidationError("Invalid credentials")


class GetAvailableCabSerializer(serializers.Serializer):
    Source_address = serializers.CharField()
    Destination_address = serializers.CharField()

    def validate(self, data):
        return data


class PassengerTravelHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelHistory
        fields = ['source_address',
                  'destination_address',
                  'booked_time',
                  'car_no']


class BookCabSerializer(serializers.Serializer):
    car_no = serializers.CharField()

    def validate(self, data):
        car_no = data.get("car_no")

        if not car_no:
            raise ValidationError("Car Number is required")
        try:
            driver = Driver.objects.get(car_no=car_no)
        except Driver.DoesNotExist:
            raise ValidationError("Car with this number does not exist")

        return data

    def create(self, validated_data):
        car_no = validated_data.pop('car_no')
        passenger_id = self.context.get("passenger_id")
        source = self.context.get("source_address")
        destination = self.context.get("destination_address")
        passenger = Passenger.objects.get(pk=passenger_id)
        driver = Driver.objects.get(car_no=car_no)
        obj1 = TravelHistory()
        obj1.passenger_id = passenger
        obj1.driver_id = driver
        obj1.car_no = driver.car_no
        obj1.source_address = source
        obj1.destination_address = destination
        obj1.save()
        obj = DriverRidesHistory()
        obj.driver_id = driver
        obj.car_no = car_no
        obj.passenger_id = passenger
        obj.source_address = source
        obj.passenger_name = passenger.first_name + passenger.last_name
        obj.destination_address = destination
        obj.save()
        return obj