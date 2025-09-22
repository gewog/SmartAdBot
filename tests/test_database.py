import pytest
from database.queries import get_all_users, inser_data, create_table

@pytest.mark.asyncio
async def test_get_all_users():
    await create_table()
    await inser_data("Test User", 123456789)
    users = await get_all_users()
    assert isinstance(users, list)
    assert 123456789 in users

# Запускаем
# pytest tests/test_database.py -v