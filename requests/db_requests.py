import psycopg2
from passlib.hash import pbkdf2_sha256
from requests.queries import Queries
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

    def register(self, username, password):
        try:
            with self.connection, self.connection.cursor() as cursor:
                cursor.execute(Queries.get_user_by_username(), (username,))
                user = cursor.fetchone()

                if user is not None:
                    return "Username already exists"

                hashed_password = pbkdf2_sha256.hash(password)
                cursor.execute(Queries.register_user(), (username, hashed_password))
        except Exception as e:
            return f"Error registering user: {str(e)}"
        finally:
            self.connection.close()

        return "User registered successfully"

    def login(self, username, password):
        try:
            with self.connection, self.connection.cursor() as cursor:
                cursor.execute(Queries.get_user_by_username(), (username,))
                user = cursor.fetchone()

                if user is None:
                    return "Invalid username or password"

                if not pbkdf2_sha256.verify(password, user[2]):
                    return "Invalid username or password"
        except Exception as e:
            return f"Error logging in: {str(e)}"
        finally:
            self.connection.close()

        return "Login successful"