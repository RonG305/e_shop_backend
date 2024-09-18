from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from category.models import Category, Subcategory
from category.serializers import CategorySerializer, SubCategorySerializer

# Create your views here.
@api_view(["GET"])
def getCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
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






# @api_view(["GET"])
# def getSubCategories(request):
   
#     sub_categories = Subcategory.objects.all()

#     serializer = SubCategorySerializer(sub_categories, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def getSubCategories(request):
    # Get the category name from the query params
    category_name = request.query_params.get("category")
    
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            sub_categories = Subcategory.objects.filter(category=category)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        sub_categories = Subcategory.objects.all()

    serializer = SubCategorySerializer(sub_categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getSubCategory(request, pk):
    try:
        subcategory = Subcategory.objects.get(pk=pk)
    except Subcategory.DoesNotExist:
        return Response({"error": "sub category with that ID is not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SubCategorySerializer(subcategory)
   
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def postSubCategory(request):
    serializer = SubCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
def updateSubCategory(request, pk):
    subcategory = Subcategory.objects.get(pk=pk)
    serializer = SubCategorySerializer(subcategory, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def deleteSubCategory(request, pk):
    try:
        subcategory = Subcategory.objects.get(pk=pk)
    except Subcategory.DoesNotExist:
        return Response({"error": " sub category with that ID is not found"}, status=status.HTTP_404_NOT_FOUND)

    subcategory.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)    
