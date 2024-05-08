from django.urls import path
from product import views

urlpatterns = [
    path("products-list/", views.getProducts, name="getProducts"),
    path("product-category/", views.getProductsByCategory, name="product-category"),
    path("product/<int:pk>/", views.getProduct, name="prodcut")
]