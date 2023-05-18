from django.urls import path
from .views import CreateUserAPIView,UsersListView,UserLoginAPIView

urlpatterns = [
    path('users/create-user/', CreateUserAPIView.as_view(), name='create-user'),
    path('users/<int:user_id>/edit/', CreateUserAPIView.as_view(), name='create-user'),
    path('users/list/', UsersListView.as_view(), name='users-list'),
    path('users/login/', UserLoginAPIView.as_view(), name='login')

]
