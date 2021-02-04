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


def dish(request, dish_id):
    """ Returns a dish with ingredients and recipe"""

    dish = get_object_or_404(Dish, pk=dish_id)
    ingredients = dish.ingredient_set.all()

    context = {"dish": dish, "ingredients": ingredients}

    return render(request, "shoppinglist/dish.html", context)


def new_dish(request):
    """ Store a new recipe """
    context = {
        "types": ["carbs", "meat", "fish", "veg"],
        "time_of_day": ["lunch", "diner", "both"],
        "name": "",
        "link": "",
        "recipe": "",
        "type": "",
        "selected_moment": "",
        "selected_type": "",
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
    return HttpResponse(data)


def delete_dish(request, dish_id):
    Dish.objects.filter(pk=dish_id).delete()
    return index(request)


def edit_dish(request, dish_id):
    # TODO: it does not edit it creates a new one
    dish = Dish.objects.filter(pk=dish_id).first()
    time_of_day_mapping = {
        1: "lunch",
        2: "both",
        3: "diner",
    }
    context = {
        "types": ["carbs", "meat", "fish", "veg"],
        "time_of_day": ["lunch", "diner", "both"],
        "name": dish.name,
        "link": dish.link,
        "recipe": dish.recipe,
        "selected_moment": time_of_day_mapping[dish.time_of_day],
        "selected_type": dish.kind,
    }
    return render(request, "shoppinglist/new_dish.html", context)
