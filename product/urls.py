from django.urls import path
from product import views

urlpatterns = [
    path("products-list/", views.getProducts, name="getProducts"),
    path("product-category/", views.getProductsByCategory, name="product-category"),
    path("product/<int:pk>/", views.getProduct, name="product"),
    path('update-product/<int:pk>/', views.updateProduct, name='update-product'),
    path('post-product/', views.postProduct, name="post-product"),
    path("delete-product/<int:pk>/", views.deleteProduct, name="delete-product"),
    path('product/barcode/<str:barcode>/', views.getProductByBarCode, name='barcode'),

    path("favourites/", views.getFavourites, name="favourites")
]
