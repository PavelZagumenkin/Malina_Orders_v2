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
    # Получить роль пользователя в таблице user_role
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
    # Установить новый пароль
    def new_role():
        return '''
        UPDATE users_role
        SET role = %s
        WHERE username = %s;
        '''