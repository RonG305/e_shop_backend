from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
