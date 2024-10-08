from django.db import models
from category.models import Category, Subcategory
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    old_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    inventory_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    barcode = models.CharField(max_length=255, unique=True, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now_add=True)
    time_created = models .TimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} - {self.category.name}"
    




    

class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"   
