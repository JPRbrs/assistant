from django.db import models


class ShoppingList(models.Model):
    """ShoppingList will store all Products to be bought. current field will mark this list
    as the next ShoppingList to be bought. When bought date_bought will be set and current
    will be set to false.
    """
    date_created = models.DateTimeField('date_created')
    current = models.BooleanField(default=False)
    date_bought = models.DateTimeField('date_bought',
                                       default=None,
                                       blank=True,
                                       null=True)

    def __str__(self):
        return self.date_created.strftime("%d-%m-%y")

    @classmethod
    def get_current(cls):
        current = cls.objects.all().filter(current=True)
        if len(current) > 1:
            # Raise exeception
            print("TODO: Two current lists found, raise exception and handle")
        return current[0]


class Product(models.Model):
    """Product will represent a single item in the shopping_list. It'll need to be passed a
    ShoppingList to be attached to
    """
    shopping_list = models.ForeignKey(ShoppingList,
                                      on_delete=models.CASCADE,
                                      default=None,
                                      blank=True,
                                      null=True)
    name = models.CharField(max_length=30)
    date_added = models.DateTimeField('date_added')

    def __str__(self):
        return self.name
