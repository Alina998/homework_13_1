import json
import os


def load_transactions(file_path):
    """Загружает данные о финансовых транзакциях из указанного JSON-файла."""
    if not os.path.isfile(file_path):
        return []

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, ValueError):
        return []
    except Exception:
        return []
