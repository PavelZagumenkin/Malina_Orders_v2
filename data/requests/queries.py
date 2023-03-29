class Queries:
    @staticmethod
    def register_user():
        return '''
        INSERT INTO users (username, password)
        VALUES (%s, %s);
        '''

    @staticmethod
    def register_role():
        return '''
        INSERT INTO users_role (username, role)
        VALUES (%s, %s);
        '''

    @staticmethod
    def get_user_by_username():
        return '''
        SELECT * FROM users WHERE username = %s;
        '''

    @staticmethod
    def get_user_role_by_username():
        return '''
        SELECT role FROM users_role WHERE username = %s;
        '''