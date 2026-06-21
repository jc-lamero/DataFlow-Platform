from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal
from datetime import date, datetime


# ---------------------------------------------------------
# Customer
# ---------------------------------------------------------

class Customer(BaseModel):
    nom: str
    email: EmailStr
    ville: str
    date_naissance: date
    date_inscription: date

    @field_validator("date_naissance")
    @classmethod
    def check_age(cls, value):
        age = (date.today() - value).days // 365
        if age < 18 or age > 80:
            raise ValueError("L'âge doit être compris entre 18 et 80 ans.")
        return value

    @field_validator("date_inscription")
    @classmethod
    def check_inscription_after_birth(cls, value, info):
        date_naissance = info.data.get("date_naissance")
        if date_naissance and value <= date_naissance:
            raise ValueError("La date d'inscription doit être postérieure à la date de naissance.")
        return value


# ---------------------------------------------------------
# Product
# ---------------------------------------------------------

class Product(BaseModel):
    nom_produit: str
    categorie_produit: Literal[
        "Électronique",
        "Vêtements",
        "Alimentation",
        "Maison",
        "Sport"
    ]
    prix: float = Field(gt=0, description="Le prix doit être strictement positif.")


# ---------------------------------------------------------
# Order
# ---------------------------------------------------------

class Order(BaseModel):
    customer_id: int
    created_at: datetime
    total_price_at: float = Field(ge=0, description="Le total ne peut pas être négatif.")
    status: Literal["en_attente", "expediee", "livree", "annulee"]

    @field_validator("created_at")
    @classmethod
    def check_not_in_future(cls, value):
        if value > datetime.now():
            raise ValueError("La date de création ne peut pas être dans le futur.")
        return value


# ---------------------------------------------------------
# OrderItem
# ---------------------------------------------------------

class OrderItem(BaseModel):
    order_id: int
    product_id: int
    quantity: int = Field(gt=0, description="La quantité doit être strictement supérieure à 0.")
    prix_unitaire: float = Field(gt=0, description="Le prix unitaire doit être strictement supérieur à 0.")
