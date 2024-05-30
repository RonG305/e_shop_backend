from django.db import models
from django.contrib.auth.models import User
import uuid

from product.models import Product

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=200)
    email_address = models.EmailField()
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)

    total_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=200, null=True, blank=True)  
    is_paid = models.BooleanField(default=False)

    paidAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} - {self.total_price}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150, blank=True, null=True) 
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=150, blank=True, null=True) 
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
