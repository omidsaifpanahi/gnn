from api.system.base_model import BaseModel

class MoleculeModel(BaseModel):
    def __init__(self):
        super().__init__('molecules')


    def get_columns(self):
        return {
            'input_type': 'enum("file","smiles") NOT NULL',
            'name': 'varchar(120) UNIQUE NOT NULL',
            'smiles' : 'text DEFAULT NULL',
            'user_id': 'int UNSIGNED NOT NULL DEFAULT 0',
            'prediction' : 'tinyint(1) UNSIGNED NOT NULL DEFAULT 0',
        }
