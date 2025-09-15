from aiogram import Router, F, Bot
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from config.config import ADMIN
from core.utils.sender_state import Steps
from core.keyboards.inline import get_confirm_button_keyboard

sender_router = Router()

@sender_router.message(Command("sender"),
                       F.from_user.id == ADMIN)
async def get_sender(message: Message, command: CommandObject,
                     state: FSMContext):
    """Тут докстринг"""
    if not command.args: # Проверка наличия аргументов
        await message.answer(f"Для создания рекламы для рассылки введите комманду /sender и имя рассылки.")
        return

    await message.answer(f"Приступим создавать рекламу для рассылки, название рекламы: {command.args} \n"
                         f"Отправь мне сообщение, которое будет использовано для рекламы")

    await state.update_data(name_adv=command.args)
    await state.set_state(Steps.message_text)

@sender_router.message(Steps.message_text)
async def message_text(message: Message, state: FSMContext):
    """Получаем рекламное сообщение, опция добавления кнопки"""
    await state.update_data(message_text=message.text)
    # data = await state.get_data()
    # await message.answer(f"Пока твоя реклама {data.get('name_adv')} имеет мообщение: \n"
    #                      f"{data.get('message_text')}")

    await message.answer(f"Я запомнил сообщение, которое ты хочешь разослать! \n"
                         f"Хочешь добавить кнопку?", reply_markup=get_confirm_button_keyboard())

    await state.update_data(message_id = message.message_id,
                            chat_id = message.from_user.id)

    await state.set_state(Steps.q_button)

@sender_router.callback_query(F.data == "add_button")
async def q_button(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Добавляем кнопку и запрашиваем текст"""
    await callback.message.answer("Отправьте текст для кнопки:", reply_markup=None)
    await state.set_state(Steps.get_text_button)


@sender_router.callback_query(F.data == "no_button")
async def q_button(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Убираем клавиатуру"""
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Ok, давай без клавиаутры")

    # Функция подтвержедния рекламного сообщения

@sender_router.message(Steps.get_text_button)
async def get_text_button(message:Message, state: FSMContext):
    """Принмаем текст для кнопки, запрашиваем ссылку"""
    await state.update_data(get_text_button = message.text)
    await message.answer("Теперь отправь ссылку для кнопик")
    await state.set_state(Steps.get_url_button)

@sender_router.message(Steps.get_url_button)
async def  get_url_button(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(get_url_button = message.text) # Сохраняю ссылку в машиеу состояний
    data = await state.get_data()
    added_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text= data.get("get_text_button"),
                                 url=f"{message.text}")
        ]
    ])
    await message.answer("bbbbb", reply_markup=added_keyboard)


