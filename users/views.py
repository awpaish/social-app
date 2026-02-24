from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        user = CustomUser.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=201)

    
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)
