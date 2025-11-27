from rest_framework import serializers
from .models import UserRegistration, Expense

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'