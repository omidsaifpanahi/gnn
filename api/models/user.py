import hashlib
from api.system.base_model import BaseModel

class UserModel(BaseModel):
    def __init__(self):
        super().__init__('users')

    @staticmethod
    def hashed_password(password):
        return hashlib.sha1(password.encode()).hexdigest()

    def get_columns(self):
        return {
            'username': 'varchar(120) UNIQUE NOT NULL',
            'password': 'varchar(120) NOT NULL',
            'role': 'tinyint  NOT NULL DEFAULT 0',
        }

    def add(self, username, password):
        password = self.hashed_password(password)
        result   = self.create({'username': username, 'password': password,'role':1})
        print(result)

    def validate(self, username, password):
        password = self.hashed_password(password)
        user = self.read({'username': username, 'password': password})
        return user
