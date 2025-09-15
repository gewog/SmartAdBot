"""Configuration module for the Telegram bot using aiogram.

This module initializes the bot and dispatcher with settings loaded from a .env file.
It also configures the Finite State Machine (FSM) storage for handling bot states.

Attributes:
    config (dict): Loaded environment variables from the .env file.
    API_TOKEN (str): Telegram Bot API token.
    bot (Bot): Aiogram Bot instance.
    dp (Dispatcher): Aiogram Dispatcher instance with MemoryStorage for FSM.
"""

from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

from aiogram.fsm.storage.memory import MemoryStorage

# Load environment variables from the .env file
config: dict = dotenv_values(r"config/.env")

# Extract the Telegram Bot API token from the config
API_TOKEN: str = config["TOKEN"]

ADMIN = int(config["ADMIN_ID"])

# Initialize the Bot instance with the API token
bot: Bot = Bot(token=API_TOKEN)

# Initialize the Dispatcher with MemoryStorage for FSM
dp: Dispatcher = Dispatcher(storage=MemoryStorage())