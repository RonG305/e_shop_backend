from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=200)
    cost = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
