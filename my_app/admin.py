from django.contrib import admin
from .models import ProductCategory, Item, ItemVariant, Product, Cart, Purchase

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Item)
admin.site.register(ItemVariant)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Purchase)
