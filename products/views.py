from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


from .serializer import (
    ProductViewSerializer,
    AddProductViewSerializer,
    UpdateProductViewSerializer,
    AddProductCategoryViewSerializer,
    UpdateProductCategoryViewSerializer,
)
from .models import Product, ProductCategory
from .filters import ProductFilter


class AddProductCategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
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
        if not product_category:
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
        if not product_category:
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
            return Response(
                {"message": "Sorry, No Products Available!"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductViewSerializer(products, many=True)
        return Response({"Products": serializer.data}, status=status.HTTP_200_OK)


class ProductByFilterView(APIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_Class = ProductFilter

    def filter_queryset(self, request, queryset):
        for backend in self.filter_backends:
            filtered_queryset = backend().filter_queryset(self, request, queryset)

        return filtered_queryset

    def get(self, request, format=None):
        qs = self.filter_queryset(self, request, Product.objects.all())
        if not qs.exists():
            return Response(
                {"message": "Sorry, No Products Available!"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductViewSerializer(qs, many=True)
        return Response(
            {"Count": qs.count(), "Products": serializer.data}, status=status.HTTP_200_OK
        )


class AddProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format: None):
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
        if not product:
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
        if not product:
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


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug, format=None):
        product = Product.objects.filter(slug=slug).first()
        if not product:
            return Response({"message": "No data available!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductViewSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug, format=None):
        product = Product.objects.filter(slug=slug).first()
        if not product:
            return Response({"message": "No data available!"}, status=status.HTTP_404_NOT_FOUND)

        if product.vendor != request.user:
            return Response(
                {"message": "You don't have permission to peform this operation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        product.delete()
        return Response({"message": "Product Deleted!"}, status=status.HTTP_200_OK)


class DeleteProductCategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, slug, format=None):
        product = ProductCategory.objects.filter(slug=slug).first()
        if not product:
            return Response({"message": "No data available!"}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff:
            return Response(
                {"message": "You don't have permission to peform this operation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        product.delete()
        return Response({"message": "Product Category Deleted!"}, status=status.HTTP_200_OK)
