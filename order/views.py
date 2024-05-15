from django.shortcuts import render
from order.models import Order
from order.serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.


@api_view(["GET"])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def getOrder(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except:
        return Response({'error': 'order does not exist'})  

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)  


@api_view(["POST"])
def createOrder(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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




