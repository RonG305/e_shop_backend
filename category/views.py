from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from category.models import Category
from category.serializers import CategorySerializer

# Create your views here.
@api_view(["GET"])
def getCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=categories)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getCategory(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"error": "category with that ID is not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category)
   
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def postCategory(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['PUT'])
def updateCategory(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def deleteCategory(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"error": "category with that ID is not found"}, status=status.HTTP_404_NOT_FOUND)

    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)    
