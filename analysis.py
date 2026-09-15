"""Анализ данных и визуализация."""

import os
import sqlite3

import pandas as pd
import matplotlib
matplotlib.use("Agg")          # рисуем в файл, без окна
import matplotlib.pyplot as plt
import networkx as nx

DB_PATH = os.path.join("data", "shop.db")
EXPORT_DIR = "exports"


def _load_orders():
    """
    Загружает все заказы в DataFrame.

    Returns
    -------
    pandas.DataFrame
        Колонки: id, client_id, product_id, date, quantity.
    """
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM orders", con)
    con.close()
    return df


def top5_clients():
    """
    Строит столбчатую диаграмму топ-5 клиентов по числу заказов.

    Сохраняет картинку в exports/top5.png.
    """
    os.makedirs(EXPORT_DIR, exist_ok=True)
    df = _load_orders()
    if df.empty:
        print("Нет заказов — нечего строить")
        return

    con = sqlite3.connect(DB_PATH)
    clients = pd.read_sql_query("SELECT id, name FROM clients", con)
    con.close()

    counts = df.groupby("client_id").size().reset_index(name="count")
    counts = counts.merge(clients, left_on="client_id", right_on="id")
    top = counts.nlargest(5, "count")

    top.plot(kind="bar", x="name", y="count",
             title="Топ-5 клиентов по числу заказов",
             legend=False, color="steelblue")
    plt.tight_layout()
    plt.savefig(os.path.join(EXPORT_DIR, "top5.png"))
    plt.close()
    print("Сохранено:", os.path.join(EXPORT_DIR, "top5.png"))


def sales_dynamics():
    """
    Строит график динамики количества заказов по датам.

    Сохраняет картинку в exports/dynamics.png.
    """
    os.makedirs(EXPORT_DIR, exist_ok=True)
    df = _load_orders()
    if df.empty:
        print("Нет заказов — нечего строить")
        return

    df["date"] = pd.to_datetime(df["date"])
    by_day = df.groupby(df["date"].dt.date).size()

    by_day.plot(title="Динамика количества заказов", marker="o")
    plt.xlabel("Дата")
    plt.ylabel("Заказов")
    plt.tight_layout()
    plt.savefig(os.path.join(EXPORT_DIR, "dynamics.png"))
    plt.close()
    print("Сохранено:", os.path.join(EXPORT_DIR, "dynamics.png"))


def client_graph():
    """
    Рисует граф связей клиентов: клиенты из одного города соединены.

    Сохраняет картинку в exports/graph.png.
    """
    os.makedirs(EXPORT_DIR, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT name, city FROM clients", con)
    con.close()

    if df.empty:
        print("Нет клиентов — нечего строить")
        return

    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row["name"], city=row["city"])

    # соединяем клиентов одного города
    for city, group in df.groupby("city"):
        names = group["name"].tolist()
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                G.add_edge(names[i], names[j])

    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color="lightblue",
            node_size=1500, font_size=10)
    plt.title("Связи клиентов (по городу)")
    plt.tight_layout()
    plt.savefig(os.path.join(EXPORT_DIR, "graph.png"))
    plt.close()
    print("Сохранено:", os.path.join(EXPORT_DIR, "graph.png"))


def build_all():
    """Запускает все виды анализа."""
    top5_clients()
    sales_dynamics()
    client_graph()


if __name__ == "__main__":
    build_all()