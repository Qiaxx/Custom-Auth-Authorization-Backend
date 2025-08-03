import hashlib

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from auth_app.authentication import authenticate

from auth_app.models import User
from auth_app.serializers import (LoginSerializer, RegisterSerializer,
                                  UserSerializer)
from auth_app.tokens import generate_token, verify_token
from auth_app.permissions import has_permission


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            try:
                user = User.objects.get(email=email, is_active=True)
            except User.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=401)

            if not user.check_password(password):
                return Response({"error": "Invalid credentials"}, status=401)

            token = generate_token(user.id)
            return Response({"token": token})

        return Response(serializer.errors, status=400)



class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Logged out"}, status=200)

# тестовая view для проверки распознавания пользователя
@api_view(['GET'])
@authenticate
def protected_view(request):
    return Response({"message": f"Welcome, {request.user.first_name}!"})

# тестовая view для проверки разрешений и ролей
@api_view(['GET'])
@authenticate
@has_permission(resource="/reports/", action="read")
def read_reports(request):
    return Response({"data": "Отчёты за август 2025 года."})

# тестовая view для проверки разрешений и ролей
@api_view(['GET'])
@authenticate
@has_permission(resource="/documents/", action="read")
def view_documents(request):
    return Response({"documents": ["doc1.pdf", "doc2.pdf"]})

# тестовая view для проверки разрешений и ролей
@api_view(['POST'])
@authenticate
@has_permission(resource="/documents/", action="write")
def create_document(request):
    return Response({"message": "Документ создан."}, status=status.HTTP_201_CREATED)

# тестовая view для проверки разрешений и ролей
@api_view(['DELETE'])
@authenticate
@has_permission(resource="/documents/", action="delete")
def delete_document(request):
    return Response({"message": "Документ удалён."}, status=status.HTTP_200_OK)
