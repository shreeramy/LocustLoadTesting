from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TodoItems
from rest_framework import status
from .serializers import TodoSerializer, RegistrationSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView

class RegistrationGenericAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)
    

class CreateTodoTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        items = TodoItems.objects.filter(user=request.user)
        serializers = TodoSerializer(
            items, 
            many=True, 
            context={'request': request}
        )
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializers = TodoSerializer(data=data,
                                    context={'request':request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        username = request.user.username
        request.user.delete()
        return Response(f"User {username} has been deleted", 
                        status=status.HTTP_200_OK)            