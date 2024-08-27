import base64
import datetime
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


# CONSUMER_KEY = settings.CONSUMER_KEY
# CONSUMER_SECRET = settings.CONSUMER_SECRET
# BUSINESS_SHORT_CODE = settings.BUSINESS_SHORT_CODE
# PASSKEY = settings.PASSKEY
# LIPA_NA_MPESA_ONLINE_URL = settings.LIPA_NA_MPESA_ONLINE_URL
# LIPA_NA_MPESA_ONLINE_AUTH_URL = settings.LIPA_NA_MPESA_ONLINE_AUTH_URL
# 174379

CONSUMER_KEY = '65hJEgJ7TYuZZwPGdGndnGagpU3Nn6AdAJFr62ddYMB0RE4h'
CONSUMER_SECRET = 'GUaqqMGOLRNAMemU3nOVesbsJn5vGdSGkSWuqaKoX2IhnhyT3bACCRhwYgpU66HV'
BUSINESS_SHORT_CODE = 174379
PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
LIPA_NA_MPESA_ONLINE_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
LIPA_NA_MPESA_ONLINE_AUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"


def get_access_token():
    response = requests.get(LIPA_NA_MPESA_ONLINE_AUTH_URL, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    access_token = response.json().get('access_token')
    return access_token

def lipa_na_mpesa_online(phone_number, amount, account_number):
    access_token = get_access_token()
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{BUSINESS_SHORT_CODE}{PASSKEY}{timestamp}".encode()).decode('utf-8')
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "BusinessShortCode": BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORT_CODE,
        "PhoneNumber": phone_number,
       "AccountReference": "ELEOSHOP", 
        "CallBackURL": "http://192.168.43.118:8000/api/payment/mpesa-confirmation/",
        "AccountReference": "Eleoshop clothline Business",
        "TransactionDesc": "Payment for ordered products at MEDSWIFT AGENCY"
    }
    response = requests.post(LIPA_NA_MPESA_ONLINE_URL, json=payload, headers=headers)
    return response.json()





