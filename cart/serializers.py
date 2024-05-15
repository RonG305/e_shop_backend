from rest_framework import serializers
from cart.models import CartItem, Cart

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'items']


class CartSerializer(serializers.ModelSerializer):        
    class Meta:
        model = Cart
        fields = "__all__"