from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings
from rest_framework.exceptions import PermissionDenied

class IsAdminOrEmployee(BasePermission):
    def has_permission(self, request, view):
        jwt_token = request.headers.get('Authorization')
        if jwt_token:
            jwt_token = jwt_token.split(' ')[1]
            # Get the user data from the JWT token payload
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_data = payload.get('user_data')
            user_type = user_data.get('UserType')
            
            if user_type == 'Administrator':
                # Allow access to all API endpoints for Administrator
                return True
            elif user_type == 'Employees':
                # Allow access to specific API endpoints for Employee
                if request.method in ['GET', 'PUT', 'PATCH']:
                    # Check if the requested employee data matches the logged-in user's data
                    employee_id = user_data.get('employee_id')
                    pk = view.kwargs.get('pk')
                    print("Employee ID:", employee_id)
                    print("PK:", pk)
                    if pk is not None and employee_id == int(pk):  # Compare employee_id with pk (converted to int)
                        return True
                    else:
                        # Deny access if the logged-in user is trying to access other employees' data
                        raise PermissionDenied("You have no access to this record.")
                return False
        return False