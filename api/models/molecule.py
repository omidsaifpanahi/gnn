from api.system.base_model import BaseModel

class MoleculeModel(BaseModel):
    def __init__(self):
        super().__init__('molecules')


    def get_columns(self):
        return {
            'name': 'varchar(120) UNIQUE NOT NULL',
            'smiles' : 'text DEFAULT NULL',
            'is_mol_file': 'tinyint(1) UNSIGNED NOT NULL DEFAULT 0',
            'user_id': 'int UNSIGNED NOT NULL DEFAULT 0'
        }
