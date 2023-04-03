import psycopg2
from passlib.hash import pbkdf2_sha256
from data.requests.queries import Queries
from config import DB_USER, DB_PASSWORD, DB_PORT, DB_HOST, DB_NAME

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def register(self, username, password, role):
        try:
            with self.connection, self.connection.cursor() as cursor:
                cursor.execute(Queries.get_user_by_username(), (username,))
                user = cursor.fetchone()

                if user is not None:
                    return "Такой логин уже существует"

                hashed_password = pbkdf2_sha256.hash(password)
                cursor.execute(Queries.register_user(), (username, hashed_password))
                cursor.execute(Queries.register_role(), (username, role))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return f"Пользователь {username} с правами {role} успешно зарегистрирован"

    def login(self, username, password):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.get_user_by_username(), (username,))
                user = cursor.fetchone()

                if user is None:
                    return "Неверный логин или пароль", None

                if not pbkdf2_sha256.verify(password, user[2]):
                    return "Неверный логин или пароль", None

                # получаем роль пользователя из таблицы user_role
                cursor.execute(Queries.get_user_role_by_username(), (username,))
                role_row = cursor.fetchone()
                role = 'None' if role_row is None else role_row[0]
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}", None
        return "Авторизация успешна", role

    def count_row_in_DB_user_role(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.get_rows_user_role())
                count_rows = cursor.fetchone()[0]
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return count_rows

    def get_users_role(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.get_users_role())
                result = cursor.fetchall()
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return result