class Session:
    __instance = None

    def __init__(self):
        if Session.__instance is not None:
            raise Exception("Невозможно создать несколько экземпляров класса Session")
        else:
            Session.__instance = self
            # self.session = None
            self.role = None

    @staticmethod
    def get_instance():
        if Session.__instance is None:
            Session()
        return Session.__instance

    # def set_session(self, session):
    #     self.session = session
    #
    # def get_session(self):
    #     return self.session

    def set_username_role(self, username, role):
        self.username = username
        self.role = role

    def get_role(self):
        return self.role

    def get_username(self):
        return self.username