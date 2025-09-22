"""
Модуль для обработки рассылок рекламных сообщений в Telegram-боте.

Этот модуль реализует логику создания, редактирования и отправки рекламных сообщений администратором.
Основные функции:
- Создание рекламного сообщения с текстом и кнопками.
- Подтверждение и отправка сообщения всем пользователям.
- Управление состояниями через FSM (finite state machine).

Зависимости:
- aiogram: Для взаимодействия с Telegram API.
- core.utils.sender_state: Состояния FSM для рассылок.
- core.keyboards.inline: Клавиатуры для взаимодействия с пользователем.
- database.queries: Запросы к базе данных для получения списка пользователей.
"""

import time

from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from config.config import ADMIN
from core.utils.sender_state import Steps
from core.keyboards.inline import get_confirm_button_keyboard, get_keyboard_for_send

from database.queries import get_all_users


sender_router = Router()


@sender_router.message(Command("sender"), F.from_user.id == ADMIN)
async def get_sender(
    message: Message, command: CommandObject, state: FSMContext
) -> None:
    """
    Обработчик команды /sender. Начинает процесс создания рекламного сообщения.

    Args:
        message (Message): Сообщение от пользователя.
        command (CommandObject): Объект команды с аргументами.
        state (FSMContext): Контекст машины состояний.

    Returns:
        None
    """
    if not command.args:  # Проверка наличия аргументов
        await message.answer(
            f"Для создания рекламы для рассылки введите комманду /sender и имя рассылки."
        )
        return

    await message.answer(
        f"Приступим создавать рекламу для рассылки, название рекламы: {command.args} \n"
        f"Отправь мне сообщение, которое будет использовано для рекламы"
    )

    await state.update_data(name_adv=command.args)
    await state.set_state(Steps.message_text)


@sender_router.message(Steps.message_text)
async def message_text(message: Message, state: FSMContext) -> None:
    """
    Получает текст рекламного сообщения и предлагает добавить кнопку.

    Args:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст машины состояний.

    Returns:
        None
    """
    await state.update_data(message_text=message.text)
    # data = await state.get_data()
    # await message.answer(f"Пока твоя реклама {data.get('name_adv')} имеет мообщение: \n"
    #                      f"{data.get('message_text')}")

    await message.answer(
        f"Я запомнил сообщение, которое ты хочешь разослать! \n"
        f"Хочешь добавить кнопку?",
        reply_markup=get_confirm_button_keyboard(),
    )

    await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)

    await state.set_state(Steps.q_button)


@sender_router.callback_query(F.data == "add_button")
async def q_button(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """
    Обрабатывает нажатие кнопки "Добавить кнопку". Запрашивает текст для кнопки.

    Args:
        callback (CallbackQuery): Колбэк-запрос от пользователя.
        bot (Bot): Экземпляр бота.
        state (FSMContext): Контекст машины состояний.

    Returns:
        None
    """
    await callback.message.answer("Отправьте текст для кнопки:", reply_markup=None)
    await state.set_state(Steps.get_text_button)


@sender_router.callback_query(F.data == "no_button")
async def q_button(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """
    Обрабатывает нажатие кнопки "Без кнопки". Подтверждает рекламное сообщение без кнопок.

    Args:
        callback (CallbackQuery): Колбэк-запрос от пользователя.
        bot (Bot): Экземпляр бота.
        state (FSMContext): Контекст машины состояний.

    Returns:
        None
    """
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Ok, давай без клавиаутры")
    data = await state.get_data()
    message_id = int(data.get("message_id"))
    chat_id = int(data.get("chat_id"))
    await confirm_post(callback.message, bot, message_id, chat_id)
    await callback.message.delete()


# Функция подтвержедния рекламного сообщения


@sender_router.message(Steps.get_text_button)
async def get_text_button(message: Message, state: FSMContext) -> None:
    """
    Получает текст для кнопки и запрашивает ссылку.

    Args:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст машины состояний.

    Returns:
        None
    """
    await state.update_data(get_text_button=message.text)
    await message.answer("Теперь отправь ссылку для кнопки")
    await state.set_state(Steps.get_url_button)


@sender_router.message(Steps.get_url_button)
async def get_url_button(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Получает ссылку для кнопки и подтверждает рекламное сообщение.

    Args:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст машины состояний.
        bot (Bot): Экземпляр бота.

    Returns:
        None
    """
    await state.update_data(
        get_url_button=message.text
    )  # Сохраняю ссылку в машину состояний
    data = await state.get_data()
    added_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=data.get("get_text_button"), url=f"{message.text}"
                )
            ]
        ]
    )
    message_id = int(data.get("message_id"))
    chat_id = int(data.get("chat_id"))
    await confirm_post(message, bot, message_id, chat_id, added_keyboard)


async def confirm_post(
    message: Message,
    bot: Bot,
    message_id: int,
    chat_id: int,
    reply_markup: InlineKeyboardMarkup = None,
) -> None:
    """
    Отправляет рекламное сообщение на подтверждение.

    Args:
        message (Message): Сообщение от пользователя.
        bot (Bot): Экземпляр бота.
        message_id (int): ID сообщения для копирования.
        chat_id (int): ID чата.
        reply_markup (InlineKeyboardMarkup, optional): Клавиатура для сообщения.

    Returns:
        None
    """
    confirmation_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data="yes")],
            [InlineKeyboardButton(text="Отклонить", callback_data="no")],
        ]
    )
    await message.answer("Ваше рекламное сообщение:")
    await bot.copy_message(chat_id, chat_id, message_id, reply_markup=reply_markup)
    await message.answer(
        f"Подтвердите рекламный пост на оправку.", reply_markup=confirmation_keyboard
    )


@sender_router.callback_query(F.data.in_(["yes", "no"]))
async def sender_decide(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """
    Обрабатывает подтверждение или отклонение рекламного сообщения.
    При подтверждении отправляет сообщение всем пользователям.

    Args:
        callback (CallbackQuery): Колбэк-запрос от пользователя.
        bot (Bot): Экземпляр бота.
        state (FSMContext): Контекст машины состояний.

    Returns:
        None
    """
    data = await state.get_data()
    # Получаю все данные
    message_id = data.get("message_id")  # не надо
    chat_id = data.get("chat_id")  # не надо
    text_button = data.get("get_text_button")
    url_button = data.get("get_url_button")
    name_advert = data.get("name_adv")
    message_text = data.get("message_text")

    if callback.data == "yes":
        await callback.message.edit_text("Начинаю рассылку", reply_markup=None)  #
        users = await get_all_users()
        print(users)
        # Логика отправки рекламного материала (я тут: создать инлайн клавиатуру, если есть ресурсы в кейб инлайн)
        for user in users:
            try:
                if text_button and url_button:
                    keyboard = await get_keyboard_for_send(text_button, url_button)

                    await bot.send_message(
                        user, f"{name_advert} \n{message_text} !!!", reply_markup=keyboard
                    )
                else:
                    await bot.send_message(user, f"{name_advert} \n*** {message_text} ***")
            except Exception as e:
                print(e)
            time.sleep(0.2)  # Пауза между сообщениями

        await callback.message.answer(f"Рекламное сообщение успешно разослано")

    elif callback.data == "no":
        await callback.message.edit_text("Как хотеть", reply_markup=None)

    await state.clear()  # Очищаю машину состояний
