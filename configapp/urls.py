from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MovieViewSet, ActorViewSet, CommentViewSet, RegisterView, VerifyOTPView, LoginView

from . import views


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'actors', ActorViewSet, basename='actor')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
