> **⚠️ NOTE: This README is a work in progress!**
> The project is still evolving, and this documentation will be expanded.
> Check back later for updates!

# SmartAdBot 🤖

**SmartAdBot** — это Telegram-бот для автоматизации рассылок рекламных сообщений с поддержкой интерактивных кнопок и управления через админ-панель. Проект разработан для упрощения маркетинговых кампаний в Telegram.

---

## 🌟 Возможности
- **Рассылка сообщений** пользователям бота.
- **Поддержка инлайн-кнопок** для интерактивных сообщений.
- **Управление через команды** (`/sender`).
- **Асинхронная работа** с базой данных PostgreSQL.
- **FSM (Finite State Machine)** для управления состояниями бота.

---

## 🛠 Стек технологий
- **Язык**: Python 3.13
- **Фреймворк**: [aiogram 3.x](https://docs.aiogram.dev/)
- **База данных**: PostgreSQL + SQLAlchemy 2.0 + AsyncPG
- **Управление зависимостями**: Poetry
- **Тестирование**: Pytest + pytest-asyncio
- **Линтинг**: Black
- **Контейнеризация**: Docker + Docker Compose

---

## 🚀 Установка и запуск

### Предварительные требования
- Установленный [Python 3.13](https://www.python.org/downloads/)
- Установленный [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/)
- Установленный [Poetry](https://python-poetry.org/docs/#installation)

---

### 1. Клонирование репозитория
```bash
git clone https://github.com/gewog/SmartAdBot.git
cd SmartAdBot
```

### 2. Настройка окружения

Создайте файл .env в корне проекта и заполните его по примеру .env.example:
```bash
TOKEN=ваш_токен_Telegram_бота
ADMIN_ID=ваш_Telegram_ID
SQLALCHEMY_URL=postgresql+asyncpg://postgres:пароль@localhost:5432/имя_базы_данных

```

### 3. Установка зависимостей
```bash
poetry install
```

### 4. Запуск через Docker (рекомендуется)
```bash
docker-compose up --build
```

### 5. Локальный запуск (без Docker)
```bash
poetry run python main.py
```

---

## 🧪 Запуск тестов
```bash
poetry run pytest tests/ -v
```

## 📌 Пример работы

1. Отправьте боту команду /start, чтобы начать взаимодействие.
2. Используйте команду /sender <название_рассылки>, чтобы создать новую рассылку.
3. Следуйте инструкциям бота для настройки сообщения и кнопок.
4. Подтвердите рассылку, и бот отправит сообщение всем пользователям.

### 📝 Автор
gewog  
📧 gewoggewog@gmail.com

### 📄 Лицензия
Проект распространяется под лицензией MIT.

<div align="center">
  <img src="https://media1.tenor.com/m/yjgMhbJ4izYAAAAC/kawaii-nice.gif" alt="Demo of SmartAdBot" width="200" />
</div>