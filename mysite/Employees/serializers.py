from rest_framework.exceptions import ValidationError
from .models import Employees, WorkSchedule
from rest_framework import serializers
from datetime import timezone
from datetime import datetime

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'
        read_only_fields = ('id', 'create_date', 'update_date')

    def validate_birthday(self, value):
        """
        Validate that the birthdate is a valid date and not a future date
        """
        today = datetime.today().date()
        try:
            if not value:
                raise serializers.ValidationError("birthdate field is required")
            elif value > today:
                raise serializers.ValidationError("birthdate cannot be a future date")
            else:
                return value
        except (TypeError, ValueError):
            raise serializers.ValidationError("invalid date format for birthdate")
    def to_internal_value(self, data):

        """
        Remove middle name and suffix fields if they are not present in request data
        """
        if 'middle_name' not in data:
            data['middlename'] = None
        if 'suffix' not in data:
            data['suffix'] = None
        return super().to_internal_value(data)
        
class WorkScheduleSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employees.objects.all())

    class Meta:
        model = WorkSchedule
        fields = '__all__'