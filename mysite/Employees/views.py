from .serializers import WorkScheduleSerializer , EmployeesSerializer
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from .models import Employees, WorkSchedule
from django.core.paginator import Paginator
from rest_framework.views import APIView
from django.http import Http404
from django.db.models import Q
from django.views import View
import datetime


class EmployeesSearch(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword', '')
        keywords = keyword.split()

        query = Q(first_name__icontains="")
        for k in keywords:
            query &= Q(first_name__icontains=k) | Q(last_name__icontains=k) | Q(middle_name__icontains=k) | Q(suffix__icontains=k)
        employees = Employees.objects.filter(query)
        if len(keywords) == 2:
            employees = employees.filter(Q(first_name__icontains=keywords[0]) & Q(last_name__icontains=keywords[1]) | Q(first_name__icontains=keywords[1]) & Q(last_name__icontains=keywords[0]))
        # Create a list of employee objects to serialize
        employee_list = [employee for employee in employees]

        # Serialize the list of employee objects
        serialized_data = EmployeesSerializer(employee_list, many=True).data
       
        page_size = request.GET.get('page_size', 10)  
        # Create a Paginator object with the filtered Employees queryset and the requested page size
        paginator = Paginator(employees, page_size)  
        # Get the "page_number" parameter from the request query string, default to 1 if not present
        page_number = request.GET.get('page_number', 1) 
        # Get a Page object for the requested page number from the Paginator object
        employees_page = paginator.get_page(page_number)
        # Serialize the Page object using the EmployeesSerializer
        serializer = EmployeesSerializer(employees_page, many=True)
        # Return the serialized data in a Response object
        return Response(serializer.data)
    
    

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'suffix','Birthday','salary', 'RegularizationDate','is_Regular')
        read_only_fields = ('id',)
        write_only_fields = ('is_Regular', 'RegularizationDate')

    def create(self, validated_data):
        return Employees.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_Regular = validated_data.get('is_Regular', instance.is_Regular)
        instance.RegularizationDate = validated_data.get('RegularizationDate', instance.RegularizationDate)
        instance.Birthday = validated_data.get('Birthday', instance.Birthday)
        instance.save()
        return instance


class EmployeeList(APIView):
    def get(self, request):
        employees = Employees.objects.all()
        serializer = EmployeesSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        employee_id = request.data.get('employee_id')
        if not Employees.objects.filter(id=employee_id).exists():
            raise Http404
        serializer = EmployeesSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       


class EmployeeDetail(APIView):
    def get_object(self, pk):
        try:
            return Employees.objects.get(pk=pk)
        except Employees.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeesSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeesSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class EmployeesRegularization(APIView):
    def get_object(self, pk):
        try:
            return Employees.objects.get(pk=pk)
        except Employees.DoesNotExist:
            return Response({'error': 'employee record does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        employee = self.get_object(pk)
        is_Regular = request.data.get('is_Regular')
        regularization_date = request.data.get('RegularizationDate')

        # Check if both columns are supplied
        if is_Regular is None or regularization_date is None:
            return Response({'error': 'Both isRegular and RegularizationDate must be supplied.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the employee is already set as regular
        if employee.is_Regular and employee.RegularizationDate is not None:
            return Response({'error': 'Employee is already set as regular.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the employee record
        data = {'is_Regular': is_Regular, 'RegularizationDate': regularization_date}
        serializer = EmployeesSerializer(employee, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CreateEmployee(APIView):
    # Create a new employee record
    def post(self, request):
        serializer = EmployeesSerializer(data=request.data)
        birthdate_str = request.data.get('birthday')
        if birthdate_str:
            try:
                birthdate = datetime.date.fromisoformat(birthdate_str)
                today = datetime.date.today()
                if birthdate < today:
                    return Response({'error': 'birthdate cannot be a future date'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'error': 'invalid date format for birthdate'}, status=status.HTTP_400_BAD_REQUEST)

        if 'middle_name' in request.data and not request.data['middle_name']:
            request.data.pop('middle_name')

        if 'suffix' in request.data and not request.data['suffix']:
            request.data.pop('suffix')

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditEmployee(APIView):
        # Get employee object based on the given primary key 'pk'
    def get_object(self, pk):
        try:
            return Employees.objects.get(pk=pk)
        except Employees.DoesNotExist:
            raise Http404
    # Partial update an employee record
    def patch(self, request, pk):
        employee = self.get_object(pk) # Retrieve employee object based on the given primary key 'pk'
        # Validating birthdate field
        birthdate_str = request.data.get('birthday')
        if birthdate_str:
            try:
                birthdate = datetime.date.fromisoformat(birthdate_str)
                today = datetime.date.today()
                if birthdate < today:
                    return Response({'error': 'birthdate cannot be a future date'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'error': 'invalid date format for birthdate'}, status=status.HTTP_400_BAD_REQUEST)
            request.data['birthday'] = birthdate.strftime('%Y-%m-%d')
        
        # Removing middle_name and suffix fields if they are not present in request data
        request_data = request.data.copy()
        request_data.pop('middle_name', None)
        request_data.pop('suffix', None)
        
        serializer = EmployeesSerializer(employee, data=request_data, partial=True) # Deserialize request data into EmployeeSerializer
        if serializer.is_valid(): # Check if the data is valid
            serializer.save() # Update the employee record with the new data
            return Response(serializer.data) # Return serialized data as response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Return error messages with status code 400 (bad request)

class DeleteEmployee(APIView):
    # Delete an employee record
    def delete(self, request, pk):
        employee = self.get_object(pk) # Retrieve employee object based on the given primary key 'pk'
        employee.delete() # Delete the employee record from the database
        return Response(status=status.HTTP_204_NO_CONTENT) # Return status code 204 (no content) as response

class WorkSchedulesView(APIView):
    def get(self, request, format=None):
        work_schedules = WorkSchedule.objects.all()
        serializer = WorkScheduleSerializer(work_schedules, many=True)
        return Response(serializer.data)
    def post(self, request):
        try:
            # Get the data from the request
            workschedule_data = request.data
            # Get a list of employee IDs from the workschedule data
            employee_id_list = [int(workschedule['employee']) for workschedule in workschedule_data]
            # Delete any existing workschedules for the specified employees
            existing_workschedule = WorkSchedule.objects.filter(employee_id__in=employee_id_list)
            existing_workschedule.delete()

            # Create a serializer for the workschedule data
            workschedule_serializer = WorkScheduleSerializer(data=workschedule_data, many=True)

            # If the serializer is valid, save the data and return a success response
            if workschedule_serializer.is_valid():
                workschedule_serializer.save()
                return Response(workschedule_serializer.data, status=status.HTTP_201_CREATED)
            else:
                # If the serializer is not valid, return an error response
                return Response(workschedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # If an error occurs, return a server error response
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class WorkScheduleCreateView(APIView):
    def post(self, request, format=None):
        serializer = WorkScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeView(APIView):
    def get(self, request, employee_id):
        try:
            # Get the employee with the specified ID
            employee = Employees.objects.get(id=employee_id)

            # Create a serializer for the employee data
            employee_serializer = EmployeesSerializer(employee)

            # Get the workschedule records for the employee
            workschedule_queryset = WorkSchedule.objects.filter(employee=employee)
            # Create a serializer for the workschedule records
            workschedule_serializer = WorkScheduleSerializer(workschedule_queryset, many=True)

            # Combine the employee and workschedule data into a single response
            response_data = {
                'employee': employee_serializer.data,
                'workschedules': workschedule_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Employees.DoesNotExist:
            return Response('Employee not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)