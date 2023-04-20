from django.urls import path
from .views import CreateUserAPIView , LoginUserAPIView

urlpatterns = [
    path('create_user/', CreateUserAPIView.as_view(), name='create_user'),
    path('login/', LoginUserAPIView.as_view())
]
