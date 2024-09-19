from django.urls import path
from order import views


urlpatterns = [
    path("getOrders/", views.getOrders, name="getOrders"),
    path('getUserOrder/', views.getOrder, name='getUserOrder'),
    path('getUserOrder_seller/', views.getOrder_Seller, name='getUserOrder_seller'),
    path("getOrder/<int:pk>/", views.getOrderId, name="getOrder"),
     path("getAllOrders/", views.getAllOrders, name="getAllOrders"),
    
    path("createOrder/", views.createOrder, name="createOrder"),
    path("createOrderForCashPayment/", views.createOrderForCashPayment, name="createOrderForCashPayment"),
    path("updateOrder/<int:pk>/", views.updateOrder, name="updateOrder"),
    path("deleteOrder/<int:pk>/", views.deleteOrder, name="deleteOrder")
]