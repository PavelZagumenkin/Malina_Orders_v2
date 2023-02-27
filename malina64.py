# -*- coding: UTF8 -*-
# !/usr/bin/env python
import psycopg2
from config import host, user, password, db_name

try:
    # Подключение к БД
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    # Создаем курсор
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM konditerskie;"
        )
        print(f"Строка: {cursor.fetchone()}")
except Exception as _ex:
    print("[INFO] Ошибка работы с БД", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] Соединение с БД закрыто")
