import pytest
import os

@pytest.fixture(autouse=True, scope="session")
def set_env_vars():
    os.environ["TOKEN"] = os.getenv("TOKEN", "")
    os.environ["ADMIN_ID"] = os.getenv("ADMIN_ID", "")
    os.environ["SQLALCHEMY_URL"] = os.getenv("SQLALCHEMY_URL", "")