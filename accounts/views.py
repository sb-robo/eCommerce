from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"messgae": "User created successully!"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({"User": "User Profile"})


class LoginView(APIView):
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
