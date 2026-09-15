"""Работа с базой данных SQLite."""

import sqlite3
import os

DB_PATH = os.path.join("data", "shop.db")


class Database:
    """Обёртка над SQLite для хранения клиентов, товаров и заказов."""

    def __init__(self, path=DB_PATH):
        """
        Parameters
        ----------
        path : str
            Путь к файлу базы данных SQLite.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path)
        self._create_tables()

    def _create_tables(self):
        """Создаёт таблицы, если их ещё нет."""
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS clients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            city TEXT)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            category TEXT)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            product_id INTEGER,
            date TEXT,
            quantity INTEGER,
            FOREIGN KEY(client_id) REFERENCES clients(id),
            FOREIGN KEY(product_id) REFERENCES products(id))""")
        self.conn.commit()

    # ---------- Клиенты ----------
    def add_client(self, client):
        """Добавляет клиента в базу. Возвращает id или None при ошибке."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO clients(name,email,phone,city) VALUES(?,?,?,?)",
                (client.name, client.email, client.phone, client.city),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.Error as e:
            print("Ошибка добавления клиента:", e)
            return None

    def get_clients(self):
        """Возвращает список всех клиентов."""
        cur = self.conn.cursor()
        cur.execute("SELECT id,name,email,phone,city FROM clients ORDER BY id")
        return cur.fetchall()

    def delete_client(self, client_id):
        """Удаляет клиента по id."""
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM clients WHERE id=?", (client_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Ошибка удаления клиента:", e)

    # ---------- Товары ----------
    def add_product(self, product):
        """Добавляет товар в базу."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO products(name,price,category) VALUES(?,?,?)",
                (product.name, product.price, product.category),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.Error as e:
            print("Ошибка добавления товара:", e)
            return None

    def get_products(self):
        """Возвращает список всех товаров."""
        cur = self.conn.cursor()
        cur.execute("SELECT id,name,price,category FROM products ORDER BY id")
        return cur.fetchall()

    # ---------- Заказы ----------
    def add_order(self, client_id, product_id, date, quantity):
        """Добавляет заказ."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO orders(client_id,product_id,date,quantity) "
                "VALUES(?,?,?,?)",
                (client_id, product_id, date, quantity),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.Error as e:
            print("Ошибка добавления заказа:", e)
            return None

    def get_orders(self):
        """Возвращает заказы с именем клиента и товара."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT o.id, c.name, p.name, o.date, o.quantity,
                   p.price * o.quantity AS total
            FROM orders o
            JOIN clients c ON c.id = o.client_id
            JOIN products p ON p.id = o.product_id
            ORDER BY o.date
        """)
        return cur.fetchall()

    # ---------- Экспорт / импорт ----------
    def export_clients_csv(self, path="exports/clients.csv"):
        """Экспортирует всех клиентов в CSV-файл."""
        import csv
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "email", "phone", "city"])
                for row in self.get_clients():
                    writer.writerow(row[1:])  # без id
            return True
        except OSError as e:
            print("Ошибка экспорта CSV:", e)
            return False

    def export_orders_json(self, path="exports/orders.json"):
        """Экспортирует все заказы в JSON-файл."""
        import json
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            data = []
            for row in self.get_orders():
                data.append({
                    "id": row[0],
                    "client": row[1],
                    "product": row[2],
                    "date": row[3],
                    "quantity": row[4],
                    "total": row[5],
                })
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except OSError as e:
            print("Ошибка экспорта JSON:", e)
            return False

    def import_clients_csv(self, path="exports/clients.csv"):
        """Импортирует клиентов из CSV-файла."""
        import csv
        from models import Client
        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    c = Client(row["name"], row["email"],
                               row["phone"], row["city"])
                    self.add_client(c)
                    count += 1
            return count
        except (OSError, KeyError) as e:
            print("Ошибка импорта CSV:", e)
            return 0

    def import_orders_json(self, path="exports/orders.json"):
        """Импортирует заказы из JSON-файла."""
        import json
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Берём id по именам
            client_by_name = {r[1]: r[0] for r in self.get_clients()}
            product_by_name = {r[1]: r[0] for r in self.get_products()}
            count = 0
            for item in data:
                cid = client_by_name.get(item.get("client"))
                pid = product_by_name.get(item.get("product"))
                if cid and pid:
                    self.add_order(cid, pid,
                                   item.get("date"),
                                   item.get("quantity", 1))
                    count += 1
            return count
        except (OSError, KeyError) as e:
            print("Ошибка импорта JSON:", e)
            return 0
    def close(self):
        """Закрывает соединение."""
        self.conn.close()


