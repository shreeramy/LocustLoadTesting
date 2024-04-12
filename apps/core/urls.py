from django.urls import path
from .views import *

urlpatterns = [
    path(
        'signup/', 
        RegistrationGenericAPIView.as_view(),
        name='register'),
    path(
        'get-items/', 
        CreateTodoTaskAPIView.as_view(),
         name='get-itmes'),
    path(
        'create-items/', 
        CreateTodoTaskAPIView.as_view(),
         name='create-itmes'),
    path(
        'delete-user/', 
        DeleteAccountAPIView.as_view(), 
        name='delete-user')
]
