
from datetime import datetime, timedelta
from rest_framework import serializers
from .models import Employees,WorkSchedules
from Users.models import Users
class WorkSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedules
        fields =  ('id', 'employee', 'date', 'time_start',
                    'time_end', 'lunch_break_start', 'lunch_break_end',
                    'created_by', 'created_datetime')
        extra_kwargs = {
            'created_by': {'required': False}
        }

class EmployeesSerializer(serializers.ModelSerializer):
    
    tenureship = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    WorkSchedules = WorkSchedulesSerializer(many=True, read_only=True)  # Nested serializer for WorkSchedules
    class Meta:
        model = Employees
        fields = ('id', 'firstname', 'middlename', 'lastname','fullname',
                   'suffix', 'birthday', 'civilstatus',
                  'created_date','created_by','updated_by', 'updated_date',  'isRegular',
                  'RegularizationDate', 'EmploymentDate', 'tenureship','WorkSchedules') #add field Workschedules
        extra_kwargs = {
            'created_by': {'required': False},
            'updated_by': {'required': False}
        }
        
    def get_fullname(self, obj):
        return f"{obj.firstname} {obj.lastname}"
    
    def get_tenureship(self, obj):
        today = datetime.now().date()
        employment_date_str = str(obj.EmploymentDate)
        employment_date = datetime.strptime(employment_date_str, '%Y-%m-%d').date()
        years_of_service = (today - employment_date) // timedelta(days=365)

        # Set the "tenureship" field value based on the employment duration
        if years_of_service < 5:
            return 'short-tenure'
        else:
            return 'long-tenure'
        
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
        if 'middle_name' not in data or data['middle_name'] in [None, '']:
            data['middlename'] = ''  # Replace None with an empty string
        else:
            data['middlename'] = data['middle_name']  # Assign the provided middle name
        
        if 'suffix' not in data or data['suffix'] in [None, '']:
            data['suffix'] = None
        return super().to_internal_value(data)

        

    
