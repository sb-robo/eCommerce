from django.urls import path
from .views import ProductView, AddProductView, AddProductCategoryView

urlpatterns = [
    path("", ProductView.as_view()),
    path("/add-product", AddProductView.as_view()),
    path("/add-productcategory", AddProductCategoryView.as_view()),
]
