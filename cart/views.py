from django.shortcuts import render, get_object_or_404
from product.models import Product
from cart.models import Cart, CartItem
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from cart.serializers import CartSerializer, CartItemSerializerView, CartItemSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# Create your views here.
# @permission_classes([IsAuthenticated])
# @api_view(['POST'])
# def addToCart(request):
#     user = request.user
#     data = request.data

#     product_id = data.get('product')
#     quantity = data.get('quantity')


#     if not product_id or not quantity:
#         return Response({'error': 'product ID and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    

    
#     try:
#         product = Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         return Response({"error": "product not found"}, status=status.HTTP_404_NOT_FOUND)  
    

#     if product.inventory_quantity < 1:
#         return Response({"error": "product run out of stock"}, status=status.HTTP_400_BAD_REQUEST)

#     cart, created = Cart.objects.get_or_create(user=user)  
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={
#         'cost': product.price,
#         'quantity': quantity
#     })

#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()

#     serializer = CartItemSerializer(cart_item)    
  

#     return Response(serializer.data, status=status.HTTP_201_CREATED)  

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addToCart(request):
    user = request.user
    data = request.data

    product_id = data.get("product")
    quantity = data.get("quantity")

    if not product_id and quantity:
        return Response({"error": "Product ID and quantity is required"}, status=status.HTTP_400_BAD_REQUEST)
        

    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product with such id not found"}, status=status.HTTP_404_NOT_FOUND)
    

    if product.inventory_quantity < 1:
        return Response({"error": "Product is out of stock"}, status=status.HTTP_400_BAD_REQUEST)


    cart, created = Cart.objects.get_or_create(user=user) 
    cart_item, created = CartItem.objects.get_or_create(product=product, defaults={
       'cost': product.price,
       'quantity': quantity
  }, cart=cart )  

    if not created:
        cart_item.quantity += 1
       
        cart_item.save()
       


    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)  




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clearCart(request):
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)


        if cart_items.exists():
            cart_items.delete()
            return Response({'message': 'cart cleared succesifully'}, status=status.HTTP_204_NO_CONTENT)
        
        else:
            return Response({'message': 'Cart is already empty'}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart could not be found'}, status=status.HTTP_200_OK)    

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def viewCart(request):
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)  

    serializer = CartSerializer(cart)
  
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cartItems(request):
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    cart_items = CartItem.objects.filter(cart=cart)

    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK) 



@api_view(['DELETE'])
def removeFromCart(request, item_id):
    user = request.user

    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    cart_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    




