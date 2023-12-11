import psycopg2
import hashlib
import os
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

    def check_version(self, version):
        try:
            with self.connection, self.connection.cursor() as cursor:
                cursor.execute(Queries.get_version())
                actual_version = cursor.fetchone()[0]
                if actual_version == version:
                    return "Текущая версия актуальна!", actual_version
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return f"Необходимо обновить приложение до версии {actual_version}!", actual_version

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

    def update_password(self, username, new_pass):
        try:
            with self.connection.cursor() as cursor:
                hashed_password = pbkdf2_sha256.hash(new_pass)
                cursor.execute(Queries.new_password(), (hashed_password, username))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return f"Пароль пользователя {username} успешно изменен."

    def update_user_role(self, username, new_role):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.new_role(), (new_role, username))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return f"Права пользователя {username} успешно изменены на {new_role}."

    def delete_user(self, username):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.delete_user(), (username, username))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return f"Пользователь {username} успешно удален из БД."

    def add_log(self, date, time, log):
        try:
            with self.connection, self.connection.cursor() as cursor:
                cursor.execute(Queries.log_entry(), (date, time, log))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return "Лог записан"

    def count_row_in_DB_logs(self, start_day, end_day):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.get_rows_logs(), (start_day, end_day))
                count_rows = cursor.fetchone()[0]
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return count_rows

    def get_logs(self, start_day, end_day):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.get_logs(), (start_day, end_day))
                result = cursor.fetchall()
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return result

    def delete_logs(self, start_day, end_day):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.delete_logs(), (start_day, end_day))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return f"Логи с {start_day} по {end_day} успешно удалены из БД."

    def count_row_in_DB_konditerskie(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.get_rows_konditerskie())
                count_rows = cursor.fetchone()[0]
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return count_rows

    def register_konditerskay(self, konditerskay_name, konditerskay_type, bakery, ice_sklad, vhod_group, tualet, tables, bakery_store):
        try:
            with self.connection, self.connection.cursor() as cursor:
                cursor.execute(Queries.get_konditerskay_by_name(), (konditerskay_name,))
                konditerskay = cursor.fetchone()
                if konditerskay is not None:
                    return "Такая кондитерская уже существует"
                cursor.execute(Queries.register_konditerskay_in_DB(), (konditerskay_name, konditerskay_type, bakery, ice_sklad, vhod_group, tualet, tables, bakery_store))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        if konditerskay_type == 0:
            type = 'Дисконт'
        else:
            type = 'Магазин'
        return f"Кондитерская {konditerskay_name} типа {type} успешно зарегистрирована"

    def get_konditerskie(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.get_konditerskie_in_DB())
                result = cursor.fetchall()
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return result

    def update_konditerskay_data(self, konditerskay_name, konditerskay_type, konditerskay_bakery, konditerskay_ice_sklad, konditerskay_vhod_group, konditerskay_tualet, konditerskay_tables, konditerskay_enable, konditerskay_bakery_store):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.update_konditerskay_in_DB(), (konditerskay_type, konditerskay_bakery, konditerskay_ice_sklad, konditerskay_vhod_group, konditerskay_tualet, konditerskay_tables, konditerskay_enable, konditerskay_bakery_store, konditerskay_name))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return f"Данные по кондитерской {konditerskay_name} успешно изменены."

    def check_period_in_prognoz(self, period, category):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.get_period_in_prognoz_in_DB(), (str(period), category))
                result = cursor.fetchall()[0]
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return result

    def check_koeff_day_week_in_DB(self, period, category):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.get_koeff_day_week_in_DB(), (str(period), category))
                result = cursor.fetchall()[0]
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return result

    def poisk_data_tovar(self, kod):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(Queries.get_data_tovar_in_DB(), (kod,))
                result = cursor.fetchall()
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            return f"Ошибка работы с БД: {str(e)}"
        return result