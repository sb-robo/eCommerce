from django_filters import rest_framework as filters
from .models import Product, ProductCategory


class ProductFilter(filters.FilterSet):
    vendor = filters.CharFilter(field_name="vendor__first_name", lookup_expr="icontains")
    category = filters.ModelChoiceFilter(
        field_name="category", to_field_name="title", queryset=ProductCategory.objects.all()
    )

    class Meta:
        model = Product
        fields = {
            "title": ["icontains"],
            "price": ["lte", "gte"],
        }
