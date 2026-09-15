"""Графический интерфейс на tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from models import Client, Product
from validators import is_valid_email, is_valid_phone


class App(tk.Tk):
    """Главное окно приложения."""

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Учёт заказов — Shop Manager")
        self.geometry("1100x700")
        self._build_ui()
        self._refresh_clients()
        self._refresh_products()
        self._refresh_orders()

    # ---------- Сборка интерфейса ----------
    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.tab_clients = ttk.Frame(notebook)
        self.tab_products = ttk.Frame(notebook)
        self.tab_orders = ttk.Frame(notebook)

        notebook.add(self.tab_clients, text="Клиенты")
        notebook.add(self.tab_products, text="Товары")
        notebook.add(self.tab_orders, text="Заказы")

        self._build_clients_tab()
        self._build_products_tab()
        self._build_orders_tab()

    def _build_clients_tab(self):
        form = ttk.LabelFrame(self.tab_clients, text="Добавить клиента")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Имя:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(form, width=20)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Email:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_email = ttk.Entry(form, width=20)
        self.entry_email.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Телефон:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_phone = ttk.Entry(form, width=20)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Город:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_city = ttk.Entry(form, width=20)
        self.entry_city.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(form, text="Добавить", command=self._add_client).grid(
            row=2, column=0, columnspan=4, pady=10
        )

        self.tree_clients = ttk.Treeview(
            self.tab_clients,
            columns=("id", "name", "email", "phone", "city"),
            show="headings",
        )
        for col, title in zip(
            ("id", "name", "email", "phone", "city"),
            ("ID", "Имя", "Email", "Телефон", "Город"),
        ):
            self.tree_clients.heading(col, text=title)
            self.tree_clients.column(col, width=140)
        self.tree_clients.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_products_tab(self):
        form = ttk.LabelFrame(self.tab_products, text="Добавить товар")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_pname = ttk.Entry(form, width=20)
        self.entry_pname.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Цена:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_price = ttk.Entry(form, width=20)
        self.entry_price.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_cat = ttk.Entry(form, width=20)
        self.entry_cat.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form, text="Добавить", command=self._add_product).grid(
            row=2, column=0, columnspan=4, pady=10
        )

        self.tree_products = ttk.Treeview(
            self.tab_products,
            columns=("id", "name", "price", "category"),
            show="headings",
        )
        for col, title in zip(
            ("id", "name", "price", "category"),
            ("ID", "Название", "Цена", "Категория"),
        ):
            self.tree_products.heading(col, text=title)
            self.tree_products.column(col, width=160)
        self.tree_products.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_orders_tab(self):
        # --- Форма создания заказа ---
        form = ttk.LabelFrame(self.tab_orders, text="Создать заказ")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Клиент:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_client = ttk.Combobox(form, state="readonly", width=25)
        self.combo_client.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Товар:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_product = ttk.Combobox(form, state="readonly", width=25)
        self.combo_product.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0,
                                                       padx=5, pady=5)
        self.entry_date = ttk.Entry(form, width=15)
        self.entry_date.insert(0, date.today().isoformat())
        self.entry_date.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Кол-во:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_qty = ttk.Entry(form, width=10)
        self.entry_qty.insert(0, "1")
        self.entry_qty.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(form, text="Создать заказ", command=self._add_order).grid(
            row=2, column=0, columnspan=4, pady=10
        )

        # --- Панель фильтров и сортировки ---
        filt = ttk.LabelFrame(self.tab_orders, text="Фильтр и сортировка")
        filt.pack(fill="x", padx=10, pady=5)

        ttk.Label(filt, text="Город:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_filter_city = ttk.Entry(filt, width=15)
        self.entry_filter_city.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filt, text="Дата от:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_date_from = ttk.Entry(filt, width=12)
        self.entry_date_from.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(filt, text="Дата до:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_date_to = ttk.Entry(filt, width=12)
        self.entry_date_to.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(filt, text="Применить",
                   command=self._refresh_orders).grid(row=0, column=6,
                                                      padx=5, pady=5)
        ttk.Button(filt, text="Сбросить",
                   command=self._reset_filters).grid(row=0, column=7,
                                                     padx=5, pady=5)

        ttk.Label(filt, text="Сортировка:").grid(row=0, column=8,
                                                 padx=5, pady=5)
        self.combo_sort = ttk.Combobox(
            filt, state="readonly", width=18,
            values=["По дате ↑", "По дате ↓",
                    "По сумме ↑", "По сумме ↓"],
        )
        self.combo_sort.current(0)
        self.combo_sort.grid(row=0, column=9, padx=5, pady=5)
        self.combo_sort.bind("<<ComboboxSelected>>",
                             lambda e: self._refresh_orders())

        # --- Таблица заказов ---
        self.tree_orders = ttk.Treeview(
            self.tab_orders,
            columns=("id", "client", "product", "date", "qty", "total"),
            show="headings",
        )
        for col, title in zip(
            ("id", "client", "product", "date", "qty", "total"),
            ("ID", "Клиент", "Товар", "Дата", "Кол-во", "Сумма"),
        ):
            self.tree_orders.heading(col, text=title)
            self.tree_orders.column(col, width=130)
        self.tree_orders.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Кнопки экспорта/импорта ---
        btns = ttk.Frame(self.tab_orders)
        btns.pack(fill="x", padx=10, pady=5)

        ttk.Button(btns, text="Экспорт клиентов CSV",
                   command=self._export_clients).pack(side="left", padx=5)
        ttk.Button(btns, text="Экспорт заказов JSON",
                   command=self._export_orders).pack(side="left", padx=5)
        ttk.Button(btns, text="Импорт клиентов CSV",
                   command=self._import_clients).pack(side="left", padx=5)
        ttk.Button(btns, text="Импорт заказов JSON",
                   command=self._import_orders).pack(side="left", padx=5)

    # ---------- Действия ----------
    def _add_client(self):
        name = self.entry_name.get().strip()
        email = self.entry_email.get().strip()
        phone = self.entry_phone.get().strip()
        city = self.entry_city.get().strip()

        if not name:
            messagebox.showerror("Ошибка", "Имя обязательно")
            return
        if not is_valid_email(email):
            messagebox.showerror("Ошибка", "Неверный email")
            return
        if not is_valid_phone(phone):
            messagebox.showerror("Ошибка", "Неверный телефон")
            return

        try:
            self.db.add_client(Client(name, email, phone, city))
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e))
            return

        for e in (self.entry_name, self.entry_email,
                  self.entry_phone, self.entry_city):
            e.delete(0, tk.END)
        self._refresh_clients()

    def _add_product(self):
        name = self.entry_pname.get().strip()
        price = self.entry_price.get().strip()
        cat = self.entry_cat.get().strip()

        if not name:
            messagebox.showerror("Ошибка", "Название обязательно")
            return
        try:
            price_val = float(price)
            if price_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка",
                                 "Цена должна быть положительным числом")
            return

        try:
            self.db.add_product(Product(name, price_val, cat))
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e))
            return

        for e in (self.entry_pname, self.entry_price, self.entry_cat):
            e.delete(0, tk.END)
        self._refresh_products()

    def _add_order(self):
        client_str = self.combo_client.get()
        product_str = self.combo_product.get()
        date_str = self.entry_date.get().strip()
        qty_str = self.entry_qty.get().strip()

        if not client_str or not product_str:
            messagebox.showerror("Ошибка", "Выберите клиента и товар")
            return

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка",
                                 "Количество должно быть положительным числом")
            return

        client_id = int(client_str.split("|")[0].strip())
        product_id = int(product_str.split("|")[0].strip())

        try:
            self.db.add_order(client_id, product_id, date_str, qty)
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e))
            return

        self._refresh_orders()

    # ---------- Экспорт / импорт ----------
    def _export_clients(self):
        try:
            ok = self.db.export_clients_csv()
            if ok:
                messagebox.showinfo(
                    "Готово", "Клиенты сохранены в exports/clients.csv")
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить CSV")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _export_orders(self):
        try:
            ok = self.db.export_orders_json()
            if ok:
                messagebox.showinfo(
                    "Готово", "Заказы сохранены в exports/orders.json")
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить JSON")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _import_clients(self):
        try:
            n = self.db.import_clients_csv()
            messagebox.showinfo("Готово", f"Импортировано клиентов: {n}")
            self._refresh_clients()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _import_orders(self):
        try:
            n = self.db.import_orders_json()
            messagebox.showinfo("Готово", f"Импортировано заказов: {n}")
            self._refresh_orders()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ---------- Обновление таблиц ----------
    def _refresh_clients(self):
        for row in self.tree_clients.get_children():
            self.tree_clients.delete(row)
        clients = self.db.get_clients()
        for row in clients:
            self.tree_clients.insert("", tk.END, values=row)

        # обновляем выпадающий список в заказах
        self.combo_client["values"] = [
            f"{r[0]} | {r[1]}" for r in clients
        ]

    def _refresh_products(self):
        for row in self.tree_products.get_children():
            self.tree_products.delete(row)
        products = self.db.get_products()
        for row in products:
            self.tree_products.insert("", tk.END, values=row)

        self.combo_product["values"] = [
            f"{r[0]} | {r[1]}" for r in products
        ]

    def _refresh_orders(self):
        """Обновляет таблицу заказов с учётом фильтров и сортировки."""
        for row in self.tree_orders.get_children():
            self.tree_orders.delete(row)

        rows = list(self.db.get_orders())
        # row = (id, client, product, date, qty, total)

        # Фильтр по городу
        city = ""
        if hasattr(self, "entry_filter_city"):
            city = self.entry_filter_city.get().strip().lower()

        date_from = ""
        date_to = ""
        if hasattr(self, "entry_date_from"):
            date_from = self.entry_date_from.get().strip()
            date_to = self.entry_date_to.get().strip()

        # Карта имя клиента → город
        cur = self.db.conn.cursor()
        cur.execute("SELECT name, city FROM clients")
        city_by_name = {r[0]: r[1] for r in cur.fetchall()}

        def keep(r):
            client_name, dt = r[1], r[3]
            if city and city_by_name.get(client_name, "").lower() != city:
                return False
            if date_from and dt < date_from:
                return False
            if date_to and dt > date_to:
                return False
            return True

        rows = [r for r in rows if keep(r)]

        # Сортировка
        if hasattr(self, "combo_sort"):
            mode = self.combo_sort.get()
            if mode == "По дате ↑":
                rows.sort(key=lambda r: r[3])
            elif mode == "По дате ↓":
                rows.sort(key=lambda r: r[3], reverse=True)
            elif mode == "По сумме ↑":
                rows.sort(key=lambda r: r[5])
            elif mode == "По сумме ↓":
                rows.sort(key=lambda r: r[5], reverse=True)

        for row in rows:
            self.tree_orders.insert("", tk.END, values=row)

    def _reset_filters(self):
        """Сбрасывает фильтры и сортировку."""
        self.entry_filter_city.delete(0, tk.END)
        self.entry_date_from.delete(0, tk.END)
        self.entry_date_to.delete(0, tk.END)
        self.combo_sort.current(0)
        self._refresh_orders()