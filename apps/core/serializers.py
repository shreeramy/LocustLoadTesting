from rest_framework import serializers
from .models import TodoItems
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class TodoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TodoItems
        fields = ['task_name']
        
    def create(self, validated_data):
        user = self.context['request'].user
        todo_item = TodoItems.objects.create(user=user, **validated_data)
        return todo_item