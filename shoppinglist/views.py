from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Dish


def index(request):
    """ List of available dishes """
    dishes = Dish.objects.all()
    context = {
        "dishes": dishes,
    }
    return render(request, "shoppinglist/index.html", context)


def recipe(request, dish_id):
    """ Returns a dish with ingredients and recipe"""

    dish = get_object_or_404(Dish, pk=dish_id)
    ingredients = dish.ingredient_set.all()

    context = {
        'dish': dish,
        'ingredients': ingredients
    }

    return render(request, 'shoppinglist/dish.html', context)
