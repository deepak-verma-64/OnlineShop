from django.contrib import admin

# Register your models here.

from .models import ProductPage, Category, Brand, Subcategory, Cart
admin.site.register(ProductPage)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Subcategory)
admin.site.register(Cart)
