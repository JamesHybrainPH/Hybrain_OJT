from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'

    def validate_employee_id(self, value):
        if self.instance and self.instance.employee_id == value:
            return value
        elif UserAccount.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee ID already exists")
        elif not UserAccount.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee ID does not exist")
        return value
        
    def validate_passphrase(self, value):
        # Perform custom password validation using Django's built-in password validation and third-party library django-password-validators
        validate_password(value)  # check length, common sequences, and other built-in validation rules
        return value
    def create(self, validated_data):

        # Get the employee ID from the validated data
        employee_id = validated_data.pop('employee_id')
        # Create a new User instance with the employee ID and validated data
        user = UserAccount(employee_id=employee_id, **validated_data)
        # Save the User instance
        user.save()
        # Return the User instance
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'useraccess', 'passphrase']