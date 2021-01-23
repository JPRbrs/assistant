from django.http import HttpResponse
from .models import Dish


def index(request):
    """ This is a test """
    return HttpResponse("Hello")


def recipe(request, dish_id):
    """ Returns a dish with ingredients and recipe"""

    dish = Dish.objects.filter(id=dish_id).first()

    ingredients = ""
    for ingredient in dish.ingredient_set.all():
        ingredients += ingredient.name + ", "

    response = (
        "Here is the recipe for {}, which has the following ingredients: {}".format(
            dish.name, ingredients
        )
    )
    return HttpResponse(response)
