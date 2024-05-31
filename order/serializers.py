from order.models import Order, OrderItem
from rest_framework import serializers
from product.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()


    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'user', 'full_name', 'email_address', 'city', 'address', 'zip_code', 'phone_number', 'total_price', 'payment_method', 'is_paid', 'paidAt', 'isDelivered', 'deliveredAt', 'createdAt', 'order_items']


class OrderSerializerView(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'user', 'full_name', 'email_address', 'city', 'address', 'zip_code', 'phone_number', 'total_price', 'payment_method', 'is_paid', 'paidAt', 'isDelivered', 'deliveredAt', 'createdAt', 'order_items']


    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        rep["user"] = str(instance.user)

        return rep