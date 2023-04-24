from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserAccount , Employees
from django.core.exceptions import ValidationError
import datetime
import re

class EmployeesSerializer(serializers.ModelSerializer):
    tenureship = serializers.SerializerMethodField()
    class Meta:
        model = Employees
        fields = ('id', 'first_name', 'middle_name', 'last_name',
                'suffix', 'birthday', 'civil_status','create_date', 'update_date','isRegular','RegularizationDate', 'EmploymentDate', 'tenureship')
        
    def get_tenureship(self, obj):
        # Calculate tenureship based on the employee's hire date
        hire_date = obj.hire_date
        today = datetime.date.today()
        years_of_service = today.year - hire_date.year - ((today.month, today.day) < (hire_date.month, hire_date.day))
        return years_of_service
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'employee_id', 'useraccess', 'passphrase', 'created_by', 'user_type')

    def validate_employee_id(self, value):
        # Check if employee_id already exists in users table
        if UserAccount.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee already has an account")
        return value
        
    def validate_passphrase(self, value):
        # Perform custom password validation using Django's built-in password validation and third-party library django-password-validators
        validate_password(value)  # check length, common sequences, and other built-in validation rules
        return value

    def validate_user_type(self, value):
        if value not in ['Administrator', 'Employee']:
            raise serializers.ValidationError("Invalid user type")
        return value

    def validate_useraccess(self, value):
        # Check if useraccess value is unique
        if UserAccount.objects.filter(useraccess=value).exists():
            raise serializers.ValidationError("Username already in use")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value
           
    def to_internal_value(self, data):
        # Try to get the internal value of the data using the base class implementation
        try:
            return super().to_internal_value(data)
        # Catch any validation errors raised by the base class implementation
        except serializers.ValidationError as exc:
            # Check if the error message contains the string "Invalid pk"
            if 'Invalid pk' in str(exc):
                # If it does, raise a new validation error with a custom error message for the employee_id field
                raise serializers.ValidationError({'employee_id': ['employee_id not exist please apply Employee']})
            # If the error message does not contain "Invalid pk", re-raise the original validation error
            raise exc
    
    def validate_useraccess(self, value):
        # Check if useraccess value is unique
        if UserAccount.objects.filter(useraccess=value).exists():
            raise serializers.ValidationError("Username already in use")
        return value
COMMON_PASSWORDS = [
    'password',
    '123456',
    'qwerty',
    'abc123',
    'letmein',
    'monkey',
    'dragon',
    'baseball',
    'football',
    'iloveyou',
]

class PassphraseSerializer(serializers.Serializer):
    passphrase = serializers.CharField()

    def validate_passphrase(self, value):
        # Check if passphrase is a common password
        if value in COMMON_PASSWORDS:
            raise serializers.ValidationError('This passphrase is too common.')

        # Check if passphrase meets Django's password validation requirements
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        # Check if passphrase is alphanumeric
        if not re.match(r'^\w+$', value):
            raise serializers.ValidationError('Passphrase must be alphanumeric.')

        # Check if passphrase is unique to this user
        user = self.context['request'].user
        if user and user.check_password(value):
            raise serializers.ValidationError('Passphrase cannot be the same as your current password.')

        return value
