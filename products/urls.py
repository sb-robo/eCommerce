from django.urls import path
from .views import (
    ProductView,
    AddProductView,
    AddProductCategoryView,
    ProductDetailView,
    DeleteProductView,
    DeleteProductCategoryView,
    UpdateProductView,
    UpdateProductCategoryView,
)

urlpatterns = [
    path("", ProductView.as_view()),
    path("add-product", AddProductView.as_view()),
    path("<slug:slug>", ProductDetailView.as_view(), name="product-detail"),
    path("update/<slug:slug>", UpdateProductView.as_view()),
    path("delete/<slug:slug>", DeleteProductView.as_view()),
    path("category/add-productcategory", AddProductCategoryView.as_view()),
    path("category/update/<slug:slug>", UpdateProductCategoryView.as_view()),
    path("category/delete/<slug:slug>", DeleteProductCategoryView.as_view()),
]
