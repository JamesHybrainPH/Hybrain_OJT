from .serializers import UserSerializer,EmployeesSerializer
from Users.authentication import BearerTokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status , viewsets
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.conf import settings
from .models import UserAccount
from datetime import timedelta
import uuid
import hashlib
import jwt
import datetime

class UsersListView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    #authentication_classes = [JWTAuthentication]
    def get(self, request):

        Users = UserAccount.objects.all()
        serializer = UserSerializer(Users, many=True)
        return Response(serializer.data)
class CreateUserAPIView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            # Generate a unique salt for each record
            salt = uuid.uuid4().hex
            # Hash the plain text password with the generated salt
            passphrase = serializer.validated_data['passphrase']
            # Encode the salted password as UTF-8 and hash it using SHA-512
            hashed_password = hashlib.sha512((passphrase + salt).encode('utf-8')).hexdigest()
            # Save the new user record to the database
            user = serializer.save(salt=salt, passphrase=hashed_password)
            # Return a response with the created user's employee_id, useraccess, and employee_id
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            errors = dict(serializer.errors)
            if 'non_field_errors' in errors:
                del errors['non_field_errors']
            # Return a response with the serializer's validation errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
class LoginUserAPIView(APIView):

    def post(self, request):
        # Get username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')     
        # Find user with given username
        try:
            user = UserAccount.objects.get(useraccess=username)
        except UserAccount.DoesNotExist:
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
        user_serializer = UserSerializer(user)
        employee_serializer = EmployeesSerializer(user.employee_id)
        serialized_user = user_serializer.data
        serialized_employee = employee_serializer.data
        
        # Remove passphrase and salt from serialized user data
        serialized_user.pop('passphrase', None)
        serialized_user.pop('salt', None)
        
        # Combine user and employee data into a single dictionary
        user_data = {**serialized_user, **serialized_employee}
        
        # Generate JWT token with expiration time of 1 hour
        jwt_payload = {
            'user_id': user.employee_id.id,
            'user_data': user_data,
            'exp': datetime.datetime.utcnow() + timedelta(hours=1)
        }
        jwt_token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm='HS256')
    
    # Return serialized user and JWT token in response
        response_data = {'user': user_data, 'jwt_token': jwt_token.decode('utf-8'),'token_id': user.employee_id.id ,'token_type': 'access', 'expires_in': 3600}
        return Response(response_data, status=status.HTTP_200_OK)

