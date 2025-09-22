import os
import pytest
from dotenv import load_dotenv

# Загружаем .env ДО любого использования os.getenv
load_dotenv()

# Теперь можно безопасно использовать os.getenv
@pytest.fixture(autouse=True, scope="session")
def set_env_vars():
    required_vars = ["TOKEN", "ADMIN_ID", "SQLALCHEMY_URL"]
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"Environment variable {var} is not set! Check GitHub Secrets.")
        os.environ[var] = value  # Убедимся, что переменная доступна