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