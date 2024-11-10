import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from api.models import user, post, molecule


def init_db():
    models = [
        user.UserModel,
        post.PostModel,
        molecule.MoleculeModel
    ]

    for model in models:
        model_instance = model()
        columns = model_instance.get_columns()
        model_instance.create_table(columns)
        print(f"Table for {model_instance.table_name} created successfully.")


if __name__ == "__main__":
    init_db()
