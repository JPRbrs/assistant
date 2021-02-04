from django.urls import path

from . import views

app_name = "shoppinglist"

urlpatterns = [
    path('', views.index, name="index"),
    path('menu', views.menu, name="menu"),
    path('dish/<int:dish_id>/', views.dish, name="dish"),
    path('dish/new_dish/', views.new_dish, name="new_dish"),
    path('dish/save_dish/', views.save_dish, name="save_dish")
]
