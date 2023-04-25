from .views import CreateUserAPIView , LoginUserAPIView , UsersListView
from django.urls import path

urlpatterns = [
    path('create_user/', CreateUserAPIView.as_view(), name='create_user'),
    path('login/', LoginUserAPIView.as_view()),
    path('users/list/', UsersListView.as_view(), name='users-list')
]
