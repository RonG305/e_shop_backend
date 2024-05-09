from rest_framework import serializers
from product.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"




class ProductSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__" 

    def to_representation(self, instance):
        repr = super().to_representation(instance)  
        repr["category"] = str(instance.category)
        return repr      