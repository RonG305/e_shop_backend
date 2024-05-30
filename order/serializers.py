from order.models import Order
from rest_framework import serializers



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', "user", "email_address"]