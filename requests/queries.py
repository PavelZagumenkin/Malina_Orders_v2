class Queries:
    @staticmethod
    def register_user():
        return '''
        INSERT INTO users (username, password)
        VALUES (%s, %s);
        '''

    @staticmethod
    def get_user_by_username():
        return '''
        SELECT * FROM users WHERE username = %s;
        '''

    @staticmethod
    def get_user_role_by_user_id():
        return '''
        SELECT role FROM user_role WHERE user_id = %s;
        '''