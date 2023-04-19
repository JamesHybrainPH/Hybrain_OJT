from django.urls import path
from .views import CreateUserAPIView , UserAccountList

urlpatterns = [
    path('create_user/', CreateUserAPIView.as_view(), name='create_user'),
    path('users/', UserAccountList.as_view(), name='user-list')
    # other paths here
]
