from django.contrib import admin
from .models import Category, Product, ProductColors, ProductEntry, CartItem, WishlistItem
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductColors)
admin.site.register(ProductEntry)
admin.site.register(CartItem)
admin.site.register(WishlistItem)