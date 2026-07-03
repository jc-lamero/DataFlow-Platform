import pytest
from datetime import date, datetime, timedelta
from pydantic import ValidationError

from validation_model import (
    Customer,
    Product,
    Order,
    OrderItem
)

# ---------------------------------------------------------
# TESTS CUSTOMER
# ---------------------------------------------------------

def test_customer_valide():
    data = {
        "nom": "Jean Dupont",
        "email": "jean.dupont@example.com",
        "ville": "Paris",
        "date_naissance": date(1990, 5, 10),
        "date_inscription": date(2020, 1, 1)
    }

    customer = Customer(**data)

    assert customer.nom == "Jean Dupont"
    assert customer.email == "jean.dupont@example.com"
    assert customer.ville == "Paris"


def test_customer_trop_jeune():
    data = {
        "nom": "Petit Paul",
        "email": "paul@example.com",
        "ville": "Lyon",
        "date_naissance": date.today().replace(year=date.today().year - 10),
        "date_inscription": date.today()
    }

    with pytest.raises(ValidationError):
        Customer(**data)


# ---------------------------------------------------------
# TESTS PRODUCT
# ---------------------------------------------------------

def test_product_valide():
    data = {
        "nom_produit": "Laptop Pro",
        "categorie_produit": "Électronique",
        "prix": 999.99
    }

    product = Product(**data)

    assert product.nom_produit == "Laptop Pro"
    assert product.prix == 999.99


def test_product_prix_negatif():
    data = {
        "nom_produit": "Laptop Pro",
        "categorie_produit": "Électronique",
        "prix": -10
    }

    with pytest.raises(ValidationError):
        Product(**data)


# ---------------------------------------------------------
# TESTS ORDER
# ---------------------------------------------------------

def test_order_valide():
    data = {
        "customer_id": 1,
        "created_at": datetime.now() - timedelta(days=10),
        "total_price_at": 120.50,
        "status": "livree"
    }

    order = Order(**data)

    assert order.customer_id == 1
    assert order.status == "livree"


def test_order_date_future():
    data = {
        "customer_id": 1,
        "created_at": datetime.now() + timedelta(days=1),  # futur → invalide
        "total_price_at": 50,
        "status": "en_attente"
    }

    with pytest.raises(ValidationError):
        Order(**data)


# ---------------------------------------------------------
# TESTS ORDERITEM
# ---------------------------------------------------------

def test_orderitem_valide():
    data = {
        "order_id": 1,
        "product_id": 2,
        "quantity": 3,
        "prix_unitaire": 19.99
    }

    item = OrderItem(**data)

    assert item.quantity == 3
    assert item.prix_unitaire == 19.99


def test_orderitem_quantite_invalide():
    data = {
        "order_id": 1,
        "product_id": 2,
        "quantity": 0,  # invalide
        "prix_unitaire": 19.99
    }

    with pytest.raises(ValidationError):
        OrderItem(**data)


def test_orderitem_prix_invalide():
    data = {
        "order_id": 1,
        "product_id": 2,
        "quantity": 2,
        "prix_unitaire": -5  # invalide
    }

    with pytest.raises(ValidationError):
        OrderItem(**data)
