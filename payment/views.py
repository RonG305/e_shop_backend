import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from payment.models import MpesaPaymentTransaction
from rest_framework import status
from payment.serializers import MpesaPaymentTransactionSerializer
import json
from payment.models import MpesaPaymentTransaction

from rest_framework.response import Response
from order.models import Order


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPaymentData(request):
    payment_data = MpesaPaymentTransaction.objects.all()
    serializers = MpesaPaymentTransactionSerializer(payment_data, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mpesa_confirmation(request):
    data = json.loads(request.body)

   
    transaction_id = data['Body']['stkCallback']['CheckoutRequestID']
    result_code = data['Body']['stkCallback']['ResultCode']
    result_desc = data['Body']['stkCallback']['ResultDesc']

    try:
        transaction = MpesaPaymentTransaction.objects.get(transaction_id=transaction_id)
        transaction.status = "paid"
        transaction.save()

        if result_code == 0:
           
            transaction.status = 'Completed'
            transaction.save()
            
            order = Order.objects.get(user=transaction.user, phone_number=transaction.phone_number)
            order.is_paid = True
            print("------------------ORDER STATUS---------", order.is_paid)
            order.save()

        return Response({"ResultCode": 0, "ResultDesc": "Accepted"})
    except MpesaPaymentTransaction.DoesNotExist:
        return Response({"ResultCode": 1, "ResultDesc": "Transaction not found"})
    

    

  
    




