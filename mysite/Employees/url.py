from .views import EmployeeList, EmployeeDetail, EmployeesRegularization, WorkSchedulesView, EmployeesView, EmployeeView
from django.urls import path 
urlpatterns = [
    path('Employees/', EmployeesView.as_view()), 
    path('Employees/<int:pk>/', EmployeeDetail.as_view(), name='employee-detail'),
    path('Employees/search/', EmployeesView.as_view()),
    path('api/employees/<int:pk>/regularize/', EmployeesRegularization.as_view()),
    path('employees/create/', EmployeesView.as_view(), name='create-employee'),
    path('employees/delete/<int:pk>/', EmployeesView.as_view(), name='delete-employee'),
    path('employees/edit/<int:pk>/', EmployeesView.as_view(), name='edit_employee'),
    path('workschedules/', WorkSchedulesView.as_view()),
    path('workschedules/create/', WorkSchedulesView.as_view(), name='workschedule-create'),
    path('workschedules/', WorkSchedulesView.as_view(), name='workschedules'),
    path('employees/<int:employee_id>/', EmployeeView.as_view(), name='employee-detail'),
    ]
    