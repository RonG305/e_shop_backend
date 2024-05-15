from django.urls import path
from order import views


urlpatterns = [
    path("getOrders/", views.getOrders, name="getOrders"),
    path("getOrder/<int:pk>/", views.getOrder, name="getOrder"),
    path("createOrder/", views.createOrder, name="createOrder"),
    path("updateOrder/<int:pk>/", views.updateOrder, name="updateOrder"),
    path("deleteOrder/<int:pk>/", views.deleteOrder, name="deleteOrder")
]