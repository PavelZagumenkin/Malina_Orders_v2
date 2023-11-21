class Queries:
    @staticmethod
    # Регистрация нового пользователя
    def register_user():
        return '''
        INSERT INTO users (username, password)
        VALUES (%s, %s);
        '''

    @staticmethod
    # Регистрация прав нового пользователя
    def register_role():
        return '''
        INSERT INTO users_role (username, role)
        VALUES (%s, %s);
        '''

    @staticmethod
    # Получить имя пользователя из БД
    def get_user_by_username():
        return '''
        SELECT * FROM users WHERE username = %s;
        '''

    @staticmethod
    # Получить права пользователя из БД
    def get_user_role_by_username():
        return '''
        SELECT role FROM users_role WHERE username = %s;
        '''

    @staticmethod
    # Получить количество строк в таблице user_role
    def get_rows_user_role():
        return '''
        SELECT COUNT(*) FROM users_role;
        '''

    @staticmethod
    # Получить роли всех пользователей с именами в таблице user_role
    def get_users_role():
        return '''
        SELECT * FROM users_role;
        '''

    @staticmethod
    # Установить новый пароль
    def new_password():
        return '''
        UPDATE users
        SET password = %s
        WHERE username = %s;
        '''

    @staticmethod
    # Установить новую роль
    def new_role():
        return '''
        UPDATE users_role
        SET role = %s
        WHERE username = %s;
        '''

    @staticmethod
    # Удалить пользователя из БД
    def delete_user():
        return '''
        DELETE FROM users_role
        WHERE username = %s;
        
        DELETE FROM users
        WHERE username = %s;
        '''

    @staticmethod
    # Запись лога
    def log_entry():
        return '''
        INSERT INTO logs (date, time, log)
        VALUES (%s, %s, %s);
        '''

    @staticmethod
    # Получить количество строк в таблице logs
    def get_rows_logs():
        return '''
        SELECT COUNT(*)
        FROM logs
        WHERE date >= %s AND date <= %s;
        '''

    @staticmethod
    # Получить все логи
    def get_logs():
        return '''
        SELECT * FROM logs
        WHERE date >= %s AND date <= %s;
        '''

    @staticmethod
    # Удалить логи из БД за период
    def delete_logs():
        return '''
        DELETE FROM logs
        WHERE date BETWEEN %s AND %s;
        '''

    @staticmethod
    # Получить имя пользователя из БД
    def get_version():
        return '''
         SELECT * FROM version;
         '''

    @staticmethod
    # Получить количество строк в таблице user_role
    def get_rows_konditerskie():
        return '''
        SELECT COUNT(*) FROM konditerskie;
        '''

    @staticmethod
    # Получить имя пользователя из БД
    def get_konditerskay_by_name():
        return '''
        SELECT * FROM konditerskie WHERE name = %s;
        '''

    @staticmethod
    # Регистрация новой кондитерской
    def register_konditerskay_in_DB():
        return '''
        INSERT INTO konditerskie (name, type, bakery, ice_sklad, vhod_group, tualet, stoliki, enable, bakery_store)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 1, %s);
        '''

    @staticmethod
    # Получить список кондитерских со всеми данными
    def get_konditerskie_in_DB():
        return '''
        SELECT * FROM konditerskie;
        '''

    @staticmethod
    # Установить новую роль
    def update_konditerskay_in_DB():
        return '''
        UPDATE konditerskie
        SET type = %s,
            bakery = %s,
            ice_sklad = %s,
            vhod_group = %s,
            tualet = %s,
            stoliki = %s,
            enable = %s,
            bakery_store = %s
        WHERE name = %s;
        '''

    @staticmethod
    # Получить все логи
    def get_period_in_prognoz_in_DB():
        return '''
        SELECT * FROM prognoz
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    # Получить все логи
    def get_koeff_day_week_in_DB():
        return '''
        SELECT * FROM koeff_day_week
        WHERE period = %s AND category = %s;
        '''


