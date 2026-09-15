"""Классы предметной области: клиент, товар, заказ."""


class Person:
    """Базовый класс человека."""

    def __init__(self, name: str, email: str, phone: str):
        """
        Parameters
        ----------
        name : str
            Имя человека.
        email : str
            Электронная почта.
        phone : str
            Номер телефона.
        """
        self._name = name
        self._email = email
        self._phone = phone

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    def __str__(self):
        return f"{self._name} <{self._email}>"


class Client(Person):
    """Клиент магазина. Наследуется от Person."""

    def __init__(self, name, email, phone, city):
        super().__init__(name, email, phone)
        self._city = city

    @property
    def city(self):
        return self._city

    def __str__(self):
        return f"Клиент: {self._name} ({self._city})"


class Product:
    """Товар магазина."""

    def __init__(self, name, price, category):
        self._name = name
        self._price = float(price)
        self._category = category

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def category(self):
        return self._category

    def __str__(self):
        return f"{self._name} — {self._price}₽"


class Order:
    """Заказ клиента."""

    def __init__(self, client, products, date, quantity=1):
        self._client = client
        self._products = products
        self._date = date
        self._quantity = quantity

    @property
    def client(self):
        return self._client

    @property
    def products(self):
        return self._products

    @property
    def date(self):
        return self._date

    @property
    def quantity(self):
        return self._quantity

    @property
    def total(self):
        """Общая стоимость заказа с учётом количества."""
        return sum(p.price for p in self._products) * self._quantity

    def __str__(self):
        return f"Заказ {self._client.name} на {self.total}₽ от {self._date}"


if __name__ == "__main__":
    # Простая проверка, что всё работает
    c = Client("Иван", "ivan@mail.ru", "+79991234567", "Москва")
    p = Product("Книга", 500, "Книги")
    o = Order(c, [p], "2026-01-15", quantity=2)
    print(c)
    print(p)
    print(o)
    print("Итого:", o.total)