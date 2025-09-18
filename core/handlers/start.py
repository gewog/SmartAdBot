from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile



base_router = Router()


@base_router.message(CommandStart())
async def answer_id(mes: types.Message):

    await mes.answer(f"Hello (◕‿◕), welcome to sender bot!")
