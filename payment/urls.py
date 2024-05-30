from django.urls import path
from payment import views

urlpatterns = [
 
    path('initiate-payment/', views.initiate_payment, name='initiate-paymet'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa-callback')
]