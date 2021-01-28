from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('menu', views.menu, name="menu"),
    path('recipe/<int:dish_id>/', views.recipe, name="recipe")
]
