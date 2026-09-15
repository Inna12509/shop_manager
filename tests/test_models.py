"""Тесты для модуля models."""

import unittest
from models import Client, Product, Order


class TestClient(unittest.TestCase):
    """Проверки класса Client."""

    def test_create_client(self):
        c = Client("Иван", "ivan@mail.ru", "+79991234567", "Москва")
        self.assertEqual(c.name, "Иван")
        self.assertEqual(c.email, "ivan@mail.ru")
        self.assertEqual(c.city, "Москва")

    def test_client_str(self):
        c = Client("Иван", "ivan@mail.ru", "+79991234567", "Москва")
        self.assertIn("Иван", str(c))
        self.assertIn("Москва", str(c))


class TestProduct(unittest.TestCase):
    """Проверки класса Product."""

    def test_price_is_float(self):
        p = Product("Книга", "500", "Книги")
        self.assertIsInstance(p.price, float)
        self.assertEqual(p.price, 500.0)


class TestOrder(unittest.TestCase):
    """Проверки класса Order."""

    def test_total_one_product(self):
        c = Client("Иван", "i@mail.ru", "+79991234567", "Москва")
        p = Product("Книга", 500, "Книги")
        o = Order(c, [p], "2026-01-15", quantity=2)
        self.assertEqual(o.total, 1000.0)

    def test_total_multiple_products(self):
        c = Client("Иван", "i@mail.ru", "+79991234567", "Москва")
        p1 = Product("Книга", 500, "Книги")
        p2 = Product("Ручка", 50, "Канцелярия")
        o = Order(c, [p1, p2], "2026-01-15", quantity=1)
        self.assertEqual(o.total, 550.0)

    def test_default_quantity(self):
        c = Client("Иван", "i@mail.ru", "+79991234567", "Москва")
        p = Product("Книга", 500, "Книги")
        o = Order(c, [p], "2026-01-15")
        self.assertEqual(o.quantity, 1)


if __name__ == "__main__":
    unittest.main()