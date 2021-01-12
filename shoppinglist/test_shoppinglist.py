from .models import Product, ShoppingList
import pytest


@pytest.mark.django_db
def test_create_product():
    p = Product(name="lechuga")
    p.save()

    assert Product.objects.get(name="lechuga").name == "lechuga"


@pytest.mark.django_db
def test_create_shopping_list():
    s = ShoppingList()

    assert s.date_created is not None
    assert s.current is False


# @pytest.mark.django_db
# def test_remove_product_from_shopping_list():
#     s = ShoppingList.get_current_list()
#     p = Product(name="lechuga")
#     p.save()

#     p.shopping_list.add(s)
