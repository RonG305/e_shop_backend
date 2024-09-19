from rest_framework import serializers
from product.models import Product, Favourites

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance) 
        rep["category"] = str(instance.category)
        rep["subcategory"] = str(instance.subcategory)  
        return rep





class ProductSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__" 

    def to_representation(self, instance):
        repr = super().to_representation(instance)  
        repr["category"] = str(instance.category)
        return repr      
    


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'    