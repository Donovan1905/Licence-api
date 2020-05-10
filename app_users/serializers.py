from rest_framework import serializers
from .models import FakeUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FakeUser
        fields = ['email', 'company']