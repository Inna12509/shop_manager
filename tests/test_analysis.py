"""Тесты для модуля analysis."""

import os
import unittest

import pandas as pd

from analysis import _load_orders


class TestLoadOrders(unittest.TestCase):
    """Проверка загрузки заказов."""

    def test_returns_dataframe(self):
        df = _load_orders()
        self.assertIsInstance(df, pd.DataFrame)

    def test_columns(self):
        df = _load_orders()
        expected = {"id", "client_id", "product_id", "date", "quantity"}
        self.assertTrue(expected.issubset(set(df.columns)))


class TestExports(unittest.TestCase):
    """Проверка, что графики создаются."""

    def test_top5_file_created(self):
        from analysis import top5_clients
        top5_clients()
        self.assertTrue(os.path.exists(os.path.join("exports", "top5.png")))


if __name__ == "__main__":
    unittest.main()