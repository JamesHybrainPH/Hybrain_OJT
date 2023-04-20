from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import status , viewsets
from .models import UserAccount
from django.views import View
import uuid
import hashlib


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateUserAPIView(APIView):
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
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Lookup user by username
        try:
            user = UserAccount.objects.get(useraccess=username, isActive=True)
        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'Username does not exist'})

# Check password
        if not check_password(password, user.passphrase):
            return JsonResponse({'error': 'Incorrect password'})

        # Get user details
        user_details = {
            'id': user.id,
            'username': user.useraccess,
            'user_type': user.user_type,
            'employee_id': user.employee_id.id,
            'first_name': user.employee_id.first_name,
            'last_name': user.employee_id.last_name,
            # add other employee fields as needed
        }

        return JsonResponse(user_details)