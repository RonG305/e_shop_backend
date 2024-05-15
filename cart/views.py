from django.shortcuts import render, get_object_or_404
from product.models import Product
from cart.models import Cart, CartItem
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from cart.serializers import CartSerializer, CartItemSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getUserCartItems(request):
    cartItems = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(cartItems, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    


@api_view(['POST'])
def createCartItem(request):
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        # Retrieve the current user
        user = request.user

        # Check if the user has an existing cart
        cart, created = Cart.objects.get_or_create(user=user)

        # If the cart already exists, retrieve it; otherwise, create a new one
        if created:
            cart.save()

      

        # Save the cart item
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def updateCartItem(request):
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        # Retrieve the current user
        user = request.user

        # Check if the user has an existing cart
        cart, created = Cart.objects.get_or_create(user=user)

        # If the cart already exists, retrieve it; otherwise, create a new one
        if created:
            cart.save()

      

        # Save the cart item
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)