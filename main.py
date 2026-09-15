"""Точка входа приложения."""

from db import Database
from gui import App


def main():
    db = Database()
    app = App(db)
    app.mainloop()
    db.close()


if __name__ == "__main__":
    main()