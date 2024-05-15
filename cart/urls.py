from django.urls import path
from cart import views

urlpatterns = [
    path('cartItems/', views.getUserCartItems, name="cartItems"),
    path('createCartItem/', views.createCartItem, name='createCartItem')
]