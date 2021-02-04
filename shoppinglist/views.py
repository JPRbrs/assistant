from django.shortcuts import render, get_object_or_404, HttpResponse
import random

from .models import Dish


def index(request):
    """ List of available dishes """
    dishes = Dish.objects.all()
    context = {
        "dishes": dishes,
    }
    return render(request, "shoppinglist/index.html", context)


def dish(request, dish_id):
    """ Returns a dish with ingredients and recipe"""

    dish = get_object_or_404(Dish, pk=dish_id)
    ingredients = dish.ingredient_set.all()

    context = {"dish": dish, "ingredients": ingredients}

    return render(request, "shoppinglist/dish.html", context)


def menu(request):
    """ Get menu for the week """
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    lunches = [lunch.name for lunch in Dish.objects.filter(time_of_day__lte=2).all()]
    random.shuffle(lunches)
    dinners = [dinner.name for dinner in Dish.objects.filter(time_of_day__gte=2).all()]
    random.shuffle(dinners)

    week = []
    for i in range(6):
        week.append({"day": days[i], "lunch": lunches[i], "dinner": dinners[i]})
    context = {"week": week}
    print(week)
    return render(request, "shoppinglist/weekly_menu.html", context)


def new_dish(request):
    """ Store a new recipe """
    context = {
        "types": ["carbs", "meat", "fish", "veg"],
        "time_of_day": ["lunch", "diner", "both"]
    }
    return render(request, "shoppinglist/new_dish.html", context)


def save_dish(request):
    data = request.POST
    time_of_day_mapping = {
        "lunch": 1,
        "both": 2,
        "diner": 3
    }
    dish = Dish(
        name=data['dish_name'],
        kind=data['type'],
        recipe=data['recipe'],
        link=data['link_to_recipe'],
        time_of_day=time_of_day_mapping[data['moment']],
    )
    dish.save()
    return HttpResponse("Dish {} saved".format(data['dish_name']))


def test(request):
    dish = get_object_or_404(Dish, pk=76)
    ingredients = dish.ingredient_set.all()

    context = {"dish": dish, "ingredients": ingredients}
    return render(request, "shoppinglist/dish.html", context)
