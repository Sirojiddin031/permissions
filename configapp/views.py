from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.serializers import serialize
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Movie, Actor, Comment
from .serializers import UserSerializer, MovieSerializer, ActorSerializer, CommentSerializer, RegisterSerializer, VerifyOTPSerializer, LoginSerializer
from .utils import send_otp, verify_otp
from .serializers import VerifyOTPSerializer
from django.shortcuts import render, redirect
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema



User = get_user_model()

class PhoneSendOTP(APIView):
    @swagger_auto_schema()
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

# class VerifySms(APIView):
#     @swagger_auto_schema(request_body=VerifySMSSerializer)
#     def post(self, request):
#         serialize = VerifySMSSerializer(data=request.data)
#         if serialize.is_valid():
#             phone_number = serialize.validated_data['phone_number']
#             verification_code = serialize.validated_data['verification_code']
#             cached_code = str(cache.get(phone_number))
#             if verification_code == str(cached_code):
#                 return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)


def send_otp_view(request):
    email = request.POST.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        save_otp(user)  # OTPni yaratish va yuborish
        return JsonResponse({"message": "OTP sent successfully!"})
    return JsonResponse({"error": "User not found!"}, status=400)


def verify_otp_view(request):
    email = request.POST.get('email')
    otp_input = request.POST.get('otp')
    user = User.objects.filter(email=email).first()
    if user and validate_otp(user, otp_input):  # OTPni tekshirish
        return JsonResponse({"message": "OTP verified successfully!"})
    return JsonResponse({"error": "Invalid OTP or OTP expired!"}, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            send_otp(phone)
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            otp = serializer.validated_data['otp']
            if verify_otp(phone, otp):
                user, created = User.objects.get_or_create(phone=phone)
                if created:
                    user.set_password(serializer.validated_data['password'])
                    user.save()
                return Response({"message": "User verified successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            user = User.objects.filter(phone=phone).first()
            if user and check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
