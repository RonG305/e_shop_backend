from django.contrib import admin

# Register your models here.
from product.models import Product, Favourites


admin.site.register(Product)
admin.site.register(Favourites)