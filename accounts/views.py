from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterStudentSerializer,
    UserUpdateSerializer,
    AdminUpdateUserSerializer,
)

User = get_user_model()

class StudentRegisterView(generics.CreateAPIView):
    """
    Public endpoint for students to register from the mobile app.
    """
    queryset = User.objects.all()
    serializer_class = RegisterStudentSerializer
    permission_classes = [permissions.AllowAny]


class SelfDetailView(generics.RetrieveUpdateAPIView):
    """
    Students and instructors can view and update their own details here.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AdminUpdateUserView(generics.RetrieveUpdateAPIView):
    """
    Admins can update any user by id.
    Uses Django's is_staff flag to gate access.
    """
    queryset = User.objects.all()
    serializer_class = AdminUpdateUserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"


class LogoutView(APIView):
    """
    Blacklist a refresh token so it cannot be used again.
    Requires the user to be authenticated.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
