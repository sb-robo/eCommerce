from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from .serializer import (
    AddProductViewSerializer,
    AddProductCategoryViewSerializer,
    ProductViewSerializer,
)
from .models import Product


class ProductView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        products = Product.objects.all()

        if not products.exists():
            return Response({"messgae": "Sorry, No Products Available!"})

        serializer = ProductViewSerializer(products)
        return Response({"Products": serializer.data}, status=status.HTTP_200_OK)


class AddProductView(APIView):
    def post(Self, request, format: None):
        serializer = AddProductViewSerializer(data=request.data, context={"conetxt": request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product added successfully!"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProductCategoryView(APIView):
    permission_classes = [IsAdminUser]

    def post(Self, request, format: None):
        serializer = AddProductCategoryViewSerializer(
            data=request.data, context={"context": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product Category added successfully!"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
