from django.shortcuts import render
from order.models import Order, OrderItem
from order.serializers import OrderSerializer, OrderSerializerView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem
from payment.mpesa_utils import lipa_na_mpesa_online
from payment.models import MpesaPaymentTransaction

# Create your views here.


@api_view(["GET"])

def getOrders(request):
    orders = Order.objects.all().order_by("-createdAt")
    orders_count = Order.objects.all().count()
    serializer = OrderSerializerView(orders, many=True)


    data = {
        "orders": serializer.data,
        "orders_count": orders_count
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrder(request):
    user = request.user

    try:
        order = Order.objects.filter(user=user).order_by("-creationTime").first()
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_204_NO_CONTENT) 
    
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrder_Seller(request):
    user = request.user

    try:
        order = Order.objects.filter(user=user).order_by("-creationTime")
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_204_NO_CONTENT) 
    
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getAllOrders(request):
    
    order = Order.objects.all().order_by("-creationTime")
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteAllOrders(request):
    orders = Order.objects.all()
    orders.delete()
    return Response({"response": "deleted succesifully"}, status=status.HTTP_204_NO_CONTENT)
    


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrderId(request, pk):

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

        phone_number = data.get('phone_number')


        order = Order(
            user=user,
            full_name=data.get('full_name'),
            email_address=data.get('email_address'),
            city=data.get('city'),
            address=data.get('address'),
            zip_code=data.get('zip_code'),
            phone_number=data.get('phone_number'),
            payment_method=data.get('payment_method'),
            total_price=0  
        )
        order.save()

        total_price = 0  
        total_cost = 0  

        for item in cart_items:
            product = item.product
            item_price = product.price * item.quantity 
            item_cost = product.old_price * item.quantity  

    
            order_item = OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item_price  
            )
            order_item.save()

     
            total_price += item_price
            total_cost += item_cost

    
            if product.inventory_quantity < item.quantity:
                return Response({"error": "Not enough items in the inventory"}, status=status.HTTP_400_BAD_REQUEST)
            product.inventory_quantity -= item.quantity
            product.save()

      
        total_profit = total_price - total_cost 

     
        order.total_price = total_price
        order.profit = total_profit
        order.save()

  
        account_number = '0220181399230'
        payment_response = lipa_na_mpesa_online(phone_number, int(total_price), account_number)
        print("Payment Response", payment_response)

        if payment_response.get('ResponseCode') != '0':
            return Response({'error': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)

        transaction_id = payment_response.get('CheckoutRequestID')


        mpesa_transaction = MpesaPaymentTransaction(
            user=user,
            phone_number=phone_number,
            amount=total_price,
            transaction_id=transaction_id,
            status="pending"
        )
        mpesa_transaction.save()

  
        cart_items.delete()


        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Cart.DoesNotExist:
        return Response({'error': 'Cart does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    # CASH PAYMENT ENDPOINT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOrderForCashPayment(request):
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
            total_price=0 
        )
        order.save()

        total_price = 0 
        total_cost = 0 

        for item in cart_items:
            product = item.product
            item_price = product.price * item.quantity  
            item_cost = product.old_price * item.quantity  

      
            order_item = OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item_price 
            )
            order_item.save()

           
            total_price += item_price
            total_cost += item_cost

       
            if product.inventory_quantity < item.quantity:
                return Response({"error": "Not enough items in the inventory"}, status=status.HTTP_400_BAD_REQUEST)
            product.inventory_quantity -= item.quantity
            product.save()

  
        total_profit = total_price - total_cost  

        order.total_price = total_price
        order.profit = total_profit
        order.save()

      
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




