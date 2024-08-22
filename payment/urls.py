from django.urls import path
from payment import views

urlpatterns = [
    path("mpesa-confirmation/", views.mpesa_confirmation, name='mpesa-confirmation'),
    path('get-payments/', views.getPaymentData, name='get-payments'),
  
]