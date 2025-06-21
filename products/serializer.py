from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, ProductCategory

User = get_user_model()


class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "title",
            "description",
            "slug",
            "price",
            "discount_price",
            "category",
            "image",
            "vendor",
        )


class AddProductCategoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = (
            "title",
            "description",
            "slug",
        )
        read_only_fields = ("slug",)

    def validate(self, attrs):
        user = self.context.get("request").user
        if not user.is_staff:
            return serializers.ValidationError(
                {"Message": "Only staffs can add new product category"}
            )

        return attrs

    def create(self, validated_data):
        product_category = ProductCategory.objects.create(**validated_data)
        return product_category


class AddProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "title",
            "description",
            "slug",
            "price",
            "discount_price",
            "category",
            "image",
            "vendor",
        )
        read_only_fields = ("slug",)

    def validate(self, attrs):
        user = self.context.get("request").user
        if not user.is_vendor:
            return serializers.ValidationError({"Message": "Only vendros can add new product"})

        price = attrs.get("price")
        discount_price = attrs.get("discount_price")

        if price < 0:
            serializers.ValidationError({"message": "Please enter a Valid price!"})

        if discount_price < 0:
            serializers.ValidationError({"message": "Please enter a Valid Discount price!"})

        return attrs

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
