from rest_framework import serializers
from cart.models import CartItem, Cart

class CartItemSerializerView(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'cost', 'product_name', 'image']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"        

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializerView(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']       

