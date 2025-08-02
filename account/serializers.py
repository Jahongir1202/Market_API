from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import uuid
from rest_framework.validators import UniqueValidator

from account.models import *

#Regrtratsiya va login

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True, write_only=True)

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password')

    def create(self, validated_data):
        phone = validated_data.pop('phone')  # Phone ni alohida olib qo'yamiz
        username = validated_data['email']
        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        # Phone ni Profile modelga yozamiz
        user.profile.phone = phone
        user.profile.save()
        return user
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
