from django.contrib import admin

from .models import Product, ShoppingList, Dish, Ingredient

admin.site.register(Product)
admin.site.register(ShoppingList)
admin.site.register(Ingredient)
admin.site.register(Dish)
