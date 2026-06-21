import psycopg2
from faker import Faker
import random
from datetime import datetime

fake = Faker("fr_FR")

# Connexion
conn = psycopg2.connect(
    dbname="dataflow_db",
    user="cyril",
    password="cyril",
    host="localhost",
    port=5432,
)
cursor = conn.cursor()

# Listes pour stocker les IDs créés
customer_ids = []
product_ids = []
order_ids = []
order_item_ids = []

# ---------------------------------------------------------
# 1) CREATE TABLE — un execute() par table
# ---------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    ville VARCHAR(100),
    date_naissance DATE,
    date_inscription DATE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    nom_produit VARCHAR(100) NOT NULL,
    categorie_produit VARCHAR(100),
    prix NUMERIC(8,2) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    created_at TIMESTAMP,
    total_price_at NUMERIC(8,2),
    status VARCHAR(20)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER,
    prix_unitaire NUMERIC(8,2)
);
""")

conn.commit()

# ---------------------------------------------------------
# 2) Génération customers + products
# ---------------------------------------------------------

categories = ["Électronique", "Vêtements", "Alimentation", "Maison", "Sport"]

for _ in range(30):

    # ----- Customers -----
    nom = fake.name()
    email = fake.email()
    ville = fake.city()
    date_naissance = fake.date_of_birth(minimum_age=18, maximum_age=80)
    date_inscription = fake.date_between(start_date="-5y", end_date="today")

    cursor.execute("""
        INSERT INTO customers (nom, email, ville, date_naissance, date_inscription)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """, (nom, email, ville, date_naissance, date_inscription))

    customer_id = cursor.fetchone()[0]
    customer_ids.append(customer_id)

    # ----- Products -----
    nom_produit = f"{fake.word().capitalize()} {fake.word().capitalize()}"
    categorie_produit = random.choice(categories)
    prix = round(random.uniform(5, 500), 2)

    cursor.execute("""
        INSERT INTO products (nom_produit, categorie_produit, prix)
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (nom_produit, categorie_produit, prix))

    product_id = cursor.fetchone()[0]
    product_ids.append(product_id)

conn.commit()

# ---------------------------------------------------------
# 3) Génération des orders + order_items
# ---------------------------------------------------------

for _ in range(30):

    # 1) Choisir un customer existant
    customer_id = random.choice(customer_ids)

    created_at = fake.date_time_between(start_date="-2y", end_date="now")
    status = random.choice(["en_attente", "expediee", "livree", "annulee"])

    # On insère l’order avec total_price_at = 0 (on mettra à jour après)
    cursor.execute("""
        INSERT INTO orders (customer_id, created_at, total_price_at, status)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (customer_id, created_at, 0, status))

    order_id = cursor.fetchone()[0]
    order_ids.append(order_id)

    # 2) Générer entre 1 et 4 order_items
    total_price = 0

    for _ in range(random.randint(1, 4)):

        product_id = random.choice(product_ids)

        # Récupérer le prix actuel du produit
        cursor.execute("SELECT prix FROM products WHERE id = %s;", (product_id,))
        prix_unitaire = cursor.fetchone()[0]

        quantity = random.randint(1, 5)

        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, prix_unitaire)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (order_id, product_id, quantity, prix_unitaire))

        item_id = cursor.fetchone()[0]
        order_item_ids.append(item_id)

        total_price += prix_unitaire * quantity

    # 3) Mise à jour du total de la commande
    cursor.execute("""
        UPDATE orders
        SET total_price_at = %s
        WHERE id = %s;
    """, (round(total_price, 2), order_id))

conn.commit()
cursor.close()
conn.close()

print("Customers créés :", customer_ids)
print("Products créés :", product_ids)
print("Orders créés :", order_ids)
print("Order items créés :", order_item_ids)
