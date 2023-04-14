from .views import CreateEmployee, EmployeeList, EmployeeDetail, EmployeesSearch, EmployeesRegularization , DeleteEmployee , EditEmployee , WorkSchedulesView , WorkScheduleCreateView , EmployeeView
from django.urls import path 
from . import views

urlpatterns = [
    path('Employees/', EmployeeList.as_view()), 
    path('Employees/<int:pk>/', EmployeeDetail.as_view()),
    path('Employees/search/', EmployeesSearch.as_view()),
    path('api/employees/<int:pk>/regularize/', EmployeesRegularization.as_view()),
    path('employees/create/', CreateEmployee.as_view(), name='create-employee'),
    path('employees/delete/<int:pk>/', DeleteEmployee.as_view(), name='delete-employee'),
    path('employees/edit/<int:pk>/', EditEmployee.as_view(), name='edit_employee'),
    path('workschedules/', WorkSchedulesView.as_view()),
    path('workschedules/create/', WorkScheduleCreateView.as_view(), name='workschedule-create'),
    path('workschedules/', WorkSchedulesView.as_view(), name='workschedules'),
    path('employees/<int:employee_id>/', EmployeeView.as_view(), name='employee-detail'),
    ]
    