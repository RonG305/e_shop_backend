from django.db import models
from django.contrib.auth.models import User
from product.models import Product



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cost = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    time_created = models.TimeField(auto_now_add=True)


    

    def __str__(self):
        return self.cart.user.username