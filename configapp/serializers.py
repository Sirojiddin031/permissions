from rest_framework import serializers
from .models import User, Movie, Actor, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import random

# User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'full_name', 'is_active', 'is_staff', 'created', 'updated']


class RegisterSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['phone', 'password', 'otp']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        otp = validated_data.pop('otp')
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user


class OTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'