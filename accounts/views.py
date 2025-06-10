from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    EditProfileSerializer,
    ChangePasswordSeralizer,
    ResetPasswordSerializer,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "User created successully!"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, context={"context": request})

        if serializer.is_valid():
            user = serializer.validated_data.get("user")

            # obtain token
            tokenSerializer = TokenObtainPairSerializer()
            tokens = tokenSerializer.get_token(user=user)
            access_token = str(tokens.access_token)
            refresh_token = str(tokens)

            return Response(
                {
                    "message": "Login Successful!",
                    "email": user.email,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logged out Successfully!"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user = ProfileSerializer(user)
        return Response({"User": user.data}, status=status.HTTP_200_OK)


class EditUserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        seralizer = EditProfileSerializer(instance=request.user, data=data)

        if seralizer.is_valid():
            seralizer.save()
            return Response({"User": seralizer.data}, status=status.HTTP_200_OK)

        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ChangePasswordSeralizer(data=request.data, instance=request.user)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ResetPasswordSerializer(data=request.data, instance=request.user)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
