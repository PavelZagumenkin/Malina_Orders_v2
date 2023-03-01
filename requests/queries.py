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
