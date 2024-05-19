from django.urls import path
from cart import views

urlpatterns = [
    path('cart/', views.viewCart, name="cart"),
    path('cart/add/', views.addToCart, name='addToCart'),
    path('cart_items/', views.cartItems, name='cart_items'),
    path('cart/remove/<int:item_id>/', views.removeFromCart, name='removeFromCart')
]