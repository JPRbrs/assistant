from django.urls import path

from . import views

app_name = "shoppinglist"

urlpatterns = [
    path('', views.index, name="index"),
    path('menu', views.menu, name="menu"),
    path('dish/<int:dish_id>/', views.dish, name="dish"),
    path('dish/new/', views.new_dish, name="new_dish"),
    path('dish/save/', views.save_dish, name="save_dish"),
    path('dish/<int:dish_id>/edit/', views.edit_dish, name="edit_dish"),
    path('dish/<int:dish_id>/delete/', views.delete_dish, name="delete_dish")
]
