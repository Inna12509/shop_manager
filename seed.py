"""Добавляет новые тестовые данные к существующей базе."""

from models import Client, Product
from db import Database

db = Database()

new_clients = [
    Client("Алексей Орлов",     "alexey@mail.ru",   "+79991112233", "Москва"),
    Client("Ксения Белова",     "ksenia@mail.ru",   "+79992223344", "Казань"),
    Client("Виктор Гусев",      "viktor@mail.ru",   "+79993334455", "Сочи"),
    Client("Наталья Зайцева",   "natalia@mail.ru",  "+79994445566", "Новосибирск"),
    Client("Роман Павлов",      "roman@mail.ru",    "+79995556677", "Санкт-Петербург"),
]

new_products = [
    Product("Клавиатура",  2500, "Электроника"),
    Product("Мышь",         800, "Электроника"),
    Product("Стол",       12000, "Мебель"),
    Product("Стул",        4500, "Мебель"),
]

existing_emails = {row[2] for row in db.get_clients()}
added_clients = 0
for c in new_clients:
    if c.email not in existing_emails:
        db.add_client(c)
        added_clients += 1

existing_products = {row[1] for row in db.get_products()}
added_products = 0
for p in new_products:
    if p.name not in existing_products:
        db.add_product(p)
        added_products += 1

print(f"Добавлено клиентов: {added_clients}")
print(f"Добавлено товаров:  {added_products}")

client_rows = db.get_clients()
product_rows = db.get_products()

client_id_by_name = {row[1]: row[0] for row in client_rows}
product_id_by_name = {row[1]: row[0] for row in product_rows}

new_orders = [
    ("Алексей Орлов",   "Клавиатура",  "2026-09-14", 1),
    ("Алексей Орлов",   "Мышь",        "2026-09-14", 2),
    ("Ксения Белова",   "Стол",        "2026-09-15", 1),
    ("Виктор Гусев",    "Стул",        "2026-09-15", 4),
    ("Наталья Зайцева", "Клавиатура",  "2026-09-16", 1),
    ("Роман Павлов",    "Мышь",        "2026-09-16", 3),
    ("Алексей Орлов",   "Стул",        "2026-09-17", 2),
    ("Ксения Белова",   "Мышь",        "2026-09-17", 1),
    ("Виктор Гусев",    "Стол",        "2026-09-18", 1),
    ("Наталья Зайцева", "Стул",        "2026-09-18", 2),
]

added_orders = 0
for c_name, p_name, date, qty in new_orders:
    cid = client_id_by_name.get(c_name)
    pid = product_id_by_name.get(p_name)
    if cid and pid:
        db.add_order(cid, pid, date, qty)
        added_orders += 1

print(f"Добавлено заказов:  {added_orders}")
print("Готово!")

db.close()