from rest_framework import serializers
from .models import Todos, Projects
from django.contrib.auth.models import User


class TodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = ['id', 'title', 'description', 'finished', 'date']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description']