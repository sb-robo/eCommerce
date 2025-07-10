from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, ProductCategory

User = get_user_model()

PRODUCT_CATEGORY_FIELDS = (
    "title",
    "description",
    "slug",
)
PRODUCT_FIELDS = (
    "title",
    "description",
    "slug",
    "price",
    "discount_price",
    "category",
    "image",
    "vendor",
)


class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = PRODUCT_FIELDS


class AddProductCategoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = PRODUCT_CATEGORY_FIELDS
        read_only_fields = ("slug",)

    def validate(self, attrs):
        user = self.context.get("request").user
        if not user.is_staff:
            raise serializers.ValidationError(
                {"Message": "Only staffs can add new product category"}
            )

        return attrs

    def create(self, validated_data):
        product_category = ProductCategory.objects.create(**validated_data)
        return product_category


class UpdateProductCategoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = PRODUCT_CATEGORY_FIELDS
        read_only_fields = ("slug",)

    def validate(self, attrs):
        user = self.context.get("request").user
        if not user.is_staff:
            raise serializers.ValidationError(
                {"Message": "Only staffs can update product category"}
            )

        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)

        instance.save()
        return instance


class AddProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = PRODUCT_FIELDS
        read_only_fields = ("slug",)

    def validate(self, attrs):
        user = self.context.get("request").user
        if not user.is_vendor:
            raise serializers.ValidationError({"Message": "Only vendors can add new product"})

        price = attrs.get("price")
        discount_price = attrs.get("discount_price")
        if price is None and price < 0:
            raise serializers.ValidationError({"message": "Please enter a Valid price!"})
        if discount_price is None and discount_price < 0:
            raise serializers.ValidationError({"message": "Please enter a Valid Discount price!"})

        return attrs

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product


class UpdateProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = PRODUCT_FIELDS
        read_only_fields = ("slug", "vendor")

    def validate(self, attrs):
        user = self.context.get("request").user
        if user != self.instance.vendor:
            raise serializers.ValidationError(
                {"Message": "You don't have permission to update this product"}
            )

        price = attrs.get("price")
        discount_price = attrs.get("discount_price")
        if price is not None and price < 0:
            raise serializers.ValidationError({"message": "Please enter a Valid price!"})
        if discount_price is not None and discount_price < 0:
            raise serializers.ValidationError({"message": "Please enter a Valid Discount price!"})

        return attrs

    def update(self, instance, validated_data):
        fields = ("title", "description", "price", "discount_price", "category", "image")

        for field in fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance
