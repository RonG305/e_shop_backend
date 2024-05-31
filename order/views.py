from django.shortcuts import render
from order.models import Order, OrderItem
from order.serializers import OrderSerializer, OrderSerializerView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem

# Create your views here.


@api_view(["GET"])

def getOrders(request):
    orders = Order.objects.all().order_by("-createdAt")
    serializer = OrderSerializerView(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
# def getOrder(request):
#     user = request.user

#     try:
#         order = Order.objects.filter(user=user).order_by("-createdAt")
#     except Order.DoesNotExist:
#         return Response({'message': 'Order not found'}, status=status.HTTP_204_NO_CONTENT) 
    
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)



def getOrder(request, pk):

    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_204_NO_CONTENT) 
    
    serializer = OrderSerializerView(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOrder(request):
    user = request.user
    data = request.data

    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order(
            user=user,
            full_name=data.get('full_name'),
            email_address=data.get('email_address'),
            city=data.get('city'),
            address=data.get('address'),
            zip_code=data.get('zip_code'),
            phone_number=data.get('phone_number'),
            payment_method=data.get('payment_method'),
            total_price=0  # Will be calculated
        )


        order.save()

        total_price = 0

        for item in cart_items:
            order_item = OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price * item.quantity
            )
            order_item.save()
            total_price += order_item.price

        order.total_price = total_price
        order.save()

        # Clear the cart after creating the order
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Cart.DoesNotExist:
        return Response({'error': 'Cart does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def updateOrder(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': "Order does not exist"})

    serializer = OrderSerializer(order, data=request.data)
    if serializer.is_valid():
        return  Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["DELETE"])
def deleteOrder(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except:
        return Response({'error': 'order does not exist'}) 
    
    order.delete()
    return Response({"success": "order deleted succesifully"}, status=status.HTTP_204_NO_CONTENT)




