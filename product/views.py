from django.shortcuts import render
from  rest_framework.response import Response
from rest_framework import status
from category.models import Category
from product.models import Product, Favourites
from product.serializers import ProductSerializer, ProductSerializerView, FavouriteSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser


from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your views here.

@receiver(post_delete, sender=Product)
@receiver(post_save, sender=Product)
def clear_cache(sender, instance, **kwrgs):
    cache.delete("cached_products")


@api_view(["GET"])
def getProducts(request):

    cached_data = cache.get("cached_products")
    if cached_data:
        print("Data from Redis")
        return Response(cached_data, status=status.HTTP_200_OK)

    print("Data from the API")
    products = Product.objects.all().order_by("-date_created", "-time_created")
    serializer = ProductSerializerView(products, many=True)

    cache.set("cached_products", serializer.data, timeout=900)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(["GET"])
def getProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response({"error": "Product with that id does not exist"})
    
    serializer = ProductSerializer(product)
   
    return Response(serializer.data, status=status.HTTP_200_OK)



# @api_view(["GET"])
# def getProductsByCategory(request):

#     category = request.GET.get('category')  # Get the category parameter from the request query string
#     products = Product.objects.all()

#     # If a category parameter is provided, filter products by that category
#     if category:
#         products = products.filter(category__name=category)

#     # Order the products 
#     products = products.order_by("-time_created", "date_created")

#     serializer = ProductSerializer(products, many=True)

   
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def getProductsByCategory(request):
    category = request.GET.get('category')      
    subcategory = request.GET.get('subcategory')  
    products = Product.objects.all()

   
    if category:
        products = products.filter(category__name=category)
    
   
    if subcategory:
        products = products.filter(subcategory__name=subcategory)


    products = products.order_by("-time_created", "date_created")

    serializer = ProductSerializerView(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def postProduct(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["PUT"])
def updateProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response({"error": "Product with that id does not exist"})
        
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["PATCH"])
def updateProductPrice(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response({"error": "Product with that id does not exist"})
    
    price_data = {"price": request.data.get("price")}
        
    serializer = ProductSerializer(product, data=price_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteProduct(requsest, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "An error occured while deleting the product"})

    product.delete()
    return Response({"message": "deleted succesifully"}, status=status.HTTP_204_NO_CONTENT)    




@api_view(['GET'])
def getFavourites(self):
    favourites = Favourites.objects.all()
    serializer = FavouriteSerializer(favourites, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
def getProductByBarCode(request, barcode):
    try:
        product = Product.objects.get(barcode=barcode)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)    


 




