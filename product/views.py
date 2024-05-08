from django.shortcuts import render
from  rest_framework.response import Response
from rest_framework import status
from category.models import Category
from product.models import Product
from product.serializers import ProductSerializer
from rest_framework.decorators import api_view

# Create your views here.


@api_view(["GET"])
def getProducts(request):
    products = Product.objects.all().order_by("-time_created", "date_created")
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(["GET"])
def getProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response({"error": "Product with that id does not exist"})
    
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
def getProductsByCategory(request):
    category = request.GET.get('category')  # Get the category parameter from the request query string
    products = Product.objects.all()

    # If a category parameter is provided, filter products by that category
    if category:
        products = products.filter(category__name=category)

    # Order the products 
    products = products.order_by("-time_created", "date_created")

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
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




