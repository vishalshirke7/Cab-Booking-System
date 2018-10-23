from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
