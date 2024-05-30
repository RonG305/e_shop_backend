import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    json_response = response.json()
    return json_response['access_token']



def lipa_na_mpesa_online(phone_number, amount, account_reference, transaction_desc):
    access_token = get_mpesa_access_token()
    api_url = f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": generate_password(),
        "Timestamp": get_timestamp(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def generate_password():
    import base64
    from datetime import datetime
    data_to_encode = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{get_timestamp()}"
    encoded_string = base64.b64encode(data_to_encode.encode())
    return encoded_string.decode('utf-8')
     
     