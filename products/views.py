from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import (
    ProductViewSerializer,
    AddProductViewSerializer,
    UpdateProductViewSerializer,
    AddProductCategoryViewSerializer,
    UpdateProductCategoryViewSerializer,
)
from .models import Product, ProductCategory


class AddProductCategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(Self, request, format=None):
        serializer = AddProductCategoryViewSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product Category added successfully!"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProductCategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def put(self, request, slug, format=None):
        product_category = ProductCategory.objects.filter(slug=slug).first()
        if not product_category.exists():
            return Response(
                {"message": "product category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateProductCategoryViewSerializer(
            data=request.data, instance=product_category, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "category updated successfully!"}, status=status.HTTP_202_ACCEPTED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug, format=None):
        product_category = ProductCategory.objects.filter(slug=slug).first()
        if not product_category.exists():
            return Response(
                {"message": "product category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateProductCategoryViewSerializer(
            data=request.data, instance=product_category, context={"request": request}, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "category updated successfully!"}, status=status.HTTP_202_ACCEPTED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        products = Product.objects.all()

        if not products.exists():
            return Response({"messgae": "Sorry, No Products Available!"})

        serializer = ProductViewSerializer(products)
        return Response({"Products": serializer.data}, status=status.HTTP_200_OK)


class AddProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(Self, request, format: None):
        serializer = AddProductViewSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product added successfully!"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, slug, format=None):
        product = Product.objects.filter(slug=slug).first()
        if not product.exists():
            return Response({"message": "product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateProductViewSerializer(
            data=request.data, instance=product, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "product updated successfully!"}, status=status.HTTP_202_ACCEPTED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug, format=None):
        product = Product.objects.filter(slug=slug).first()
        if not product.exists():
            return Response({"message": "product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateProductViewSerializer(
            data=request.data, instance=product, context={"request": request}, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "product updated successfully!"}, status=status.HTTP_202_ACCEPTED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
