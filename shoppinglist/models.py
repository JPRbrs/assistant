""" Models for shopping list app"""

from django.db import models
from django.utils import timezone


class ShoppingList(models.Model):
    """ShoppingList will store all Products to be bought. current field will mark this list
    as the next ShoppingList to be bought. When bought date_bought will be set and current
    will be set to false.
    """

    date_created = models.DateTimeField("date_created")
    current = models.BooleanField(default=False)
    date_bought = models.DateTimeField(
        "date_bought", default=None, blank=True, null=True
    )

    def __init__(self):
        super().__init__()
        self.date_created = timezone.now()
        self.current = False

    def __str__(self):
        return self.date_created.strftime("%d-%m-%y")

    def delete_item(self, item_to_remove):
        """ Delete item from current shopping list"""
        self.product_set.filter(name=item_to_remove).delete()

    @classmethod
    def get_current_list(cls):
        """Gets the list for the next visit to the supermarket"""
        current = cls.objects.all().filter(current=True)
        if len(current) > 1:
            # Raise exeception
            print("TODO: Two current lists found, raise exception and handle")
        return current[0]

    def add_item(self, item_name):
        """ Add item to current shopping_list"""
        product = Product(name=item_name,
                          shopping_list=self,
                          date_added=timezone.now())
        product.save()

    def list_items(self):
        return [p['name'] for p in self.product_set.all().values()]

    def clear_list(self):
        for item in self.product_set.all():
            item.delete()

    def mark_list_as_done(self):
        self.date_bought = timezone.now()
        self.current = False


class Product(models.Model):
    """Product will represent a single item in the shopping_list."""

    name = models.CharField(max_length=30)
    shopping_list = models.ManyToManyField(ShoppingList)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Dish(models.Model):
    """Dish will represent a lunch or dinner option"""

    name = models.CharField(max_length=40)
    # TODO: Restrict options to meat, fish, veg, pasta, rice, pulses
    kind = models.CharField(max_length=30)
    recipe = models.CharField(max_length=1000, default=None, blank=True, null=True)
    # 1 for lunch, 3 for dinner, 2 for both
    time_of_day = models.IntegerField(default=False)
    # Link to recipe online or locally (pictures and screenshots)
    link = models.CharField(max_length=100, default=None, null=True)


    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredients will represent a single item in the Dish model."""

    name = models.CharField(max_length=30)
    season = models.CharField(max_length=6, default=None, null=True)
    dish = models.ManyToManyField(Dish)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

# >>> i.dish.all()
# <QuerySet [<Dish: pasta>]>
# >>> d.ingredient_set.all()
# <QuerySet [<Ingredient: pasta>, <Ingredient: tomate>]>
