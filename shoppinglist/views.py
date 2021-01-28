from django.shortcuts import render, get_object_or_404
import random

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


def menu(request):

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    lunches = [lunch.name for lunch in Dish.objects.filter(time_of_day__lte=2).all()]
    random.shuffle(lunches)
    dinners = [dinner.name for dinner in Dish.objects.filter(time_of_day__gte=2).all()]
    random.shuffle(dinners)

    week = []
    for i in range(6):
        week.append({'day': days[i], 'lunch': lunches[i], 'dinner': dinners[i]})
    context = {
        'week': week
    }
    print(week)
    return render(request, 'shoppinglist/weekly_menu.html', context)
