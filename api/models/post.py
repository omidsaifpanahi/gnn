from api.system.base_model import BaseModel

class PostModel(BaseModel):
    def __init__(self):
        super().__init__('posts')

    def get_columns(self):
        return {
            'title': 'varchar(120) NOT NULL',
            'tags' : 'varchar(255) DEFAULT NULL',
            'description': 'text DEFAULT NULL',
        }
