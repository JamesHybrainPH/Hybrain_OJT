#class UsersListView modules ------
import uuid
import hashlib
#class UserLoginAPIView modules ------
import datetime
from datetime import timedelta

import jwt
from django.conf import settings



from Users.authentication import BearerTokenAuthentication
from .permission import IsAdminOrEmployee

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from rest_framework.exceptions import AuthenticationFailed


from .serializers import UsersSerializer,EmployeesSerializer
from .models import Users



class UsersListView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAdminOrEmployee]
    #authentication_classes = [JWTAuthentication]
    def get(self, request):

        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)  

class CreateUserAPIView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    #permission_classes = [IsAdminOrEmployee]

    def post(self, request):
       
        # Initialize serializer with request data and context
        serializer = UsersSerializer(data=request.data, context={'request': request})

        # Check if the serializer is valid
        if serializer.is_valid():
            # Generate a unique salt for each record
            salt = uuid.uuid4().hex

            # Hash the plain text password with the generated salt
            password = serializer.validated_data['passphrase']
            # Encode the salted password as UTF-8 and hash it using SHA-512
            hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

            # Save the new user record to the database
            user = serializer.save(salt=salt, passphrase=hashed_password)
            user_type = serializer.data['UserType']
            # Create a response data dictionary with the created user's employee_id, useraccess, and employee name
            response_data = {
                'UserType': user_type,
                'employee_id': user.employee_id.id,
                'salt': user.salt,
                'useraccess': user.useraccess,
                'passphrase': user.passphrase,
            }

            # Return a response with the response data and a status of HTTP 201 CREATED
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # If the serializer is invalid, extract the validation errors
            errors = dict(serializer.errors)
            if 'non_field_errors' in errors:
                del errors['non_field_errors']
            # Return a response with the serializer's validation errors and a status of HTTP 400 BAD REQUEST
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, user_id):
        # Get the user object from the database
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            # If the user is not found, return an HTTP 404 NOT FOUND response
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Initialize serializer with user object and updated request data
        serializer = UsersSerializer(user, data=request.data, partial=True, context={'request': request})

        # Check if the serializer is valid
        if serializer.is_valid():
            # Generate a new salt and hash the updated password if it is included in the request data
            if 'passphrase' in serializer.validated_data:
                salt = uuid.uuid4().hex
                password = serializer.validated_data['passphrase']
                hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
                serializer.validated_data['salt'] = salt
                serializer.validated_data['passphrase'] = hashed_password

            # Save the updated user record to the database
            user = serializer.save()

            # Create a response data dictionary with the updated user's employee_id, useraccess, and employee name
            response_data = {
                'UserType': user.UserType,
                'employee_id': user.employee_id.id,
                'useraccess': user.useraccess,
            }

            # Return a response with the response data and a status of HTTP 200 OK
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # If the serializer is invalid, extract the validation errors
            errors = dict(serializer.errors)
            if 'non_field_errors' in errors:
                del errors['non_field_errors']
            # Return a response with the serializer's validation errors and a status of HTTP 400 BAD REQUEST
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        
        # Get username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')     
        # Find user with given username
        try:
            user = Users.objects.get(useraccess=username)
        except Users.DoesNotExist:
            return Response({'error': 'Username does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user is active
        if not user.isActive:
            return Response({'error': 'Account is disabled'}, status=status.HTTP_403_FORBIDDEN)
        
        # Verify password
        salt = user.salt
        hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

        if hashed_password != user.passphrase:
            return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Serialize user and employee data
        user_serializer = UsersSerializer(user)
        employee_serializer = EmployeesSerializer(user.employee_id)
        serialized_user = user_serializer.data
        serialized_employee = employee_serializer.data
        
        # Remove passphrase and salt from serialized user data
        serialized_user.pop('passphrase', None)
        serialized_user.pop('salt', None)
        serialized_user.pop('created_by', None)
        # Combine user and employee data into a single dictionary
        user_data = {**serialized_user, **serialized_employee}
   
        # Generate JWT token with expiration time of 1 hour
        jwt_payload = {
            'user_id': user.employee_id.id,
            'full_name': user_serializer.data['full_name'],
            'created_by':user_serializer.data['full_name'],
            'updated_by':user_serializer.data['full_name'],
            'user_data': user_data,
            'exp': datetime.datetime.utcnow() + timedelta(hours=1)
        }
        jwt_token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm='HS256')
        # Return serialized user and JWT token in response
        response_data = {'user': user_data, 'jwt_token': jwt_token, 'token_id': user.employee_id.id, 'token_type': 'access', 'expires_in': 3600}
        return Response(response_data, status=status.HTTP_200_OK)