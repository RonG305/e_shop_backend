from django.shortcuts import render
from django_daraja.mpesa.core import MpesaClient
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from payment.mpesa_utils import lipa_na_mpesa_online
from payment.models import MpesaTransaction
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    user = request.user
    phone_number = request.data.get("phone_number")
    amount = request.data.get("amount")
    account_reference = request.data.get("account_reference")
    transaction_desc = request.data.get("transaction_desc")

    response = lipa_na_mpesa_online(phone_number, amount, account_reference, transaction_desc)


    if response['ResponseCode'] == '0':
        MpesaTransaction.objects.create(
            user=user,
            phone_number=phone_number,
            amount=amount,
            transaction_id=response['order_id'],
            status="pending"
        )
        return  Response({"message": "Payment initiated succesifully"})
    return Response({"error": "Payment initialization failed"})


def mpesa_callback(request):
    data = request.data
    checkout_request_id = data['Body']['stkCallback']['order_id']
    result_code = data['Body']['stkCallback']['ResultCode']
    result_desc = data['Body']['stkCallback']['ResultDesc']


    try:
        transaction = MpesaTransaction.objects.get(transaction_id=checkout_request_id)
        if result_code == 0:
            transaction.status = "success"
        else:
            transaction.status = 'Failed'
        transaction.save()
        return Response({'message': 'callback received succesifully'}, status=200)
    except MpesaTransaction.DoesNotExist:
        return Response({'error': 'transaction not found'}, status=400)            




