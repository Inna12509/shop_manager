"""Проверка email и телефона через регулярные выражения."""

import re

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
PHONE_RE = re.compile(r"^\+?\d{10,15}$")


def is_valid_email(email: str) -> bool:
    """
    Проверяет, похож ли email на настоящий.

    Parameters
    ----------
    email : str
        Строка для проверки.

    Returns
    -------
    bool
        True, если email валиден, иначе False.
    """
    return bool(EMAIL_RE.match(email or ""))


def is_valid_phone(phone: str) -> bool:
    """
    Проверяет, похож ли номер телефона на настоящий.

    Разрешены: опциональный + в начале, затем 10–15 цифр.

    Parameters
    ----------
    phone : str
        Строка для проверки.

    Returns
    -------
    bool
        True, если телефон валиден, иначе False.
    """
    return bool(PHONE_RE.match(phone or ""))


if __name__ == "__main__":
    # Проверяем работу
    print(is_valid_email("test@mail.ru"))     # True
    print(is_valid_email("bad-email"))        # False
    print(is_valid_email("a@b.c"))            # True
    print(is_valid_phone("+79991234567"))     # True
    print(is_valid_phone("89991234567"))      # True
    print(is_valid_phone("123"))              # False
    print(is_valid_phone("abc"))              # False