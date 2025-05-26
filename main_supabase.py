#!/usr/bin/env python3
"""
Фитнес-помощник для тренеров - Telegram Bot (Supabase версия)
Основной файл для запуска бота с Supabase
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Добавляем корневую папку проекта в путь
sys.path.append(str(Path(__file__).parent.parent))

# Загружаем переменные окружения для Supabase
def load_supabase_env():
    """Загрузка .env файла для Supabase"""
    env_path = Path(__file__).parent.parent / '.env.supabase'
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print(f"✅ Переменные окружения Supabase загружены")
    else:
        print(f"⚠️ Файл .env.supabase не найден")

load_supabase_env()

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Импортируем конфигурацию Supabase после загрузки env
from shared.config_supabase import supabase_config

# Настройка логирования с поддержкой Unicode
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Настройка консоли для Windows
if sys.platform == 'win32':
    import os
    os.system('chcp 65001 > nul')  # Переключаем консоль на UTF-8
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=supabase_config.BOT_TOKEN)
dp = Dispatcher()

# Основной роутер
main_router = Router()

@main_router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start с поддержкой Supabase"""
    # Проверяем или создаем тренера в Supabase
    from shared.supabase_database import SupabaseTrainerService
    
    user_id = str(message.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    if not trainer:
        # Создаем нового тренера в Supabase
        trainer = await SupabaseTrainerService.create_trainer(
            telegram_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        logger.info(f"👤 Новый тренер зарегистрирован в Supabase: {trainer.first_name}")
    
    welcome_text = f"""
🏋️‍♂️ Добро пожаловать в фитнес-помощник!

Привет, {message.from_user.first_name}! 

Я помогу вам эффективно управлять тренировками и клиентами.

☁️ <b>Powered by Supabase</b> - все ваши данные надежно сохранены в облаке!

🚀 <b>Возможности:</b>
• 👥 Управление клиентами
• 💪 Планирование тренировок  
• 📊 Аналитика и отчеты
• 🍎 Планы питания
• 💰 Финансовый учет

Для начала работы используйте команды в меню или нажмите /help
"""
    
    # Создаем клавиатуру с веб-приложением
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="🌐 Открыть веб-приложение",
            web_app=WebAppInfo(url=supabase_config.WEB_APP_URL)
        )
    )
    keyboard.row(
        InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
        InlineKeyboardButton(text="👥 Клиенты", callback_data="clients")
    )
    keyboard.row(
        InlineKeyboardButton(text="💪 Тренировки", callback_data="workouts"),
        InlineKeyboardButton(text="📊 Статистика", callback_data="stats")
    )
    
    await message.answer(
        welcome_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )

@main_router.message(Command("help"))
async def cmd_help(message: Message):
    """Помощь по командам"""
    help_text = """
<b>🤖 Команды бота (Supabase версия):</b>

/start - Главное меню
/help - Эта справка
/profile - Профиль тренера
/clients - Управление клиентами
/workouts - Тренировки
/stats - Статистика

<b>☁️ Supabase преимущества:</b>
• Облачное хранение данных
• Синхронизация между устройствами
• Масштабируемость и надежность
• Real-time обновления

<b>🌐 Веб-приложение:</b>
Полный функционал доступен через веб-приложение:
• Детальная аналитика
• Конструктор программ
• Планировщик питания
• Финансовая отчетность

<b>📱 Быстрые действия:</b>
• Добавление клиента
• Планирование тренировки
• Отправка программы
• Напоминания

<b>💡 Совет:</b> Используйте кнопки меню для быстрого доступа!
"""
    
    await message.answer(help_text, parse_mode="HTML")

@main_router.message(Command("profile"))
async def cmd_profile(message: Message):
    """Профиль тренера с данными из Supabase"""
    from shared.supabase_database import SupabaseTrainerService, SupabaseClientService, SupabaseWorkoutService
    
    user_id = str(message.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    if not trainer:
        await message.answer("❌ Тренер не найден. Выполните /start для регистрации.")
        return
    
    # Получаем статистику из Supabase
    clients_count = await SupabaseClientService.get_clients_count(trainer.id)
    workouts_count = await SupabaseWorkoutService.get_workouts_count(trainer.id)
    
    profile_text = f"""
👤 <b>Профиль тренера</b>

<b>Основная информация:</b>
• Имя: {trainer.first_name} {trainer.last_name or ''}
• Username: @{trainer.username or 'не указан'}
• ID: {trainer.telegram_id}

<b>📊 Статистика (из Supabase):</b>
• Клиентов: {clients_count}
• Тренировок проведено: {workouts_count}
• Дата регистрации: {trainer.created_at.strftime('%d.%m.%Y')}

<b>⚙️ Настройки:</b>
• Уведомления: включены
• Язык: русский
• База данных: ☁️ Supabase

Для полной настройки профиля используйте веб-приложение.
"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="⚙️ Настроить профиль",
            web_app=WebAppInfo(url=f"{supabase_config.WEB_APP_URL}#/settings")
        )
    )
    
    await message.answer(profile_text, reply_markup=keyboard.as_markup(), parse_mode="HTML")

@main_router.message(Command("clients"))
async def cmd_clients(message: Message):
    """Управление клиентами через Supabase"""
    from shared.supabase_database import SupabaseTrainerService, SupabaseClientService
    
    user_id = str(message.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    if not trainer:
        await message.answer("❌ Тренер не найден. Выполните /start для регистрации.")
        return
    
    clients_count = await SupabaseClientService.get_clients_count(trainer.id)
    
    clients_text = f"""
👥 <b>Управление клиентами</b>

📊 <b>Статистика:</b>
• Всего клиентов в Supabase: {clients_count}

<b>Что можно делать:</b>
• ➕ Добавить нового клиента
• 📋 Просмотреть список клиентов
• 📊 Отслеживать прогресс
• 📝 Вести заметки

☁️ Все данные автоматически синхронизируются с Supabase.

Откройте веб-приложение для полного функционала управления клиентами.
"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="👥 Управление клиентами",
            web_app=WebAppInfo(url=f"{supabase_config.WEB_APP_URL}#/clients")
        )
    )
    keyboard.row(
        InlineKeyboardButton(text="➕ Добавить клиента", callback_data="client_add"),
        InlineKeyboardButton(text="📋 Список клиентов", callback_data="client_list")
    )
    
    await message.answer(clients_text, reply_markup=keyboard.as_markup(), parse_mode="HTML")

@main_router.message(Command("workouts"))
async def cmd_workouts(message: Message):
    """Тренировки с данными из Supabase"""
    from shared.supabase_database import SupabaseTrainerService, SupabaseWorkoutService
    
    user_id = str(message.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    if not trainer:
        await message.answer("❌ Тренер не найден. Выполните /start для регистрации.")
        return
    
    # Получаем статистику тренировок из Supabase
    today_workouts = await SupabaseWorkoutService.get_today_workouts(trainer.id)
    upcoming_workouts = await SupabaseWorkoutService.get_upcoming_workouts(trainer.id, limit=5)
    total_workouts = await SupabaseWorkoutService.get_workouts_count(trainer.id)
    
    workouts_text = f"""
💪 <b>Тренировки</b>

<b>📊 Статистика (из Supabase):</b>
• Всего тренировок: {total_workouts}
• Сегодня: {len(today_workouts)}
• Ближайших: {len(upcoming_workouts)}

<b>📅 На сегодня:</b>
"""
    
    if today_workouts:
        for workout in today_workouts:
            time_str = workout.scheduled_date.strftime('%H:%M')
            workouts_text += f"• {time_str} - {workout.client.first_name} {workout.client.last_name or ''}\n"
    else:
        workouts_text += "Нет запланированных тренировок\n"
    
    workouts_text += """
<b>🔧 Возможности:</b>
• 📅 Планирование тренировок
• 🏃‍♂️ Отслеживание прогресса
• 📝 Заметки после тренировок
• ⏰ Напоминания клиентам

☁️ Все данные автоматически сохраняются в Supabase.

Используйте веб-приложение для создания детальных программ тренировок.
"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="💪 Планировщик тренировок",
            web_app=WebAppInfo(url=f"{supabase_config.WEB_APP_URL}#/workouts")
        )
    )
    keyboard.row(
        InlineKeyboardButton(text="➕ Создать тренировку", callback_data="workout_add"),
        InlineKeyboardButton(text="📅 На сегодня", callback_data="workout_today")
    )
    
    await message.answer(workouts_text, reply_markup=keyboard.as_markup(), parse_mode="HTML")

@main_router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Статистика из Supabase"""
    from shared.supabase_database import SupabaseTrainerService, SupabaseClientService, SupabaseWorkoutService
    
    user_id = str(message.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    if not trainer:
        await message.answer("❌ Тренер не найден. Выполните /start для регистрации.")
        return
    
    # Получаем всю статистику из Supabase
    clients_count = await SupabaseClientService.get_clients_count(trainer.id)
    workouts_count = await SupabaseWorkoutService.get_workouts_count(trainer.id)
    today_workouts = await SupabaseWorkoutService.get_today_workouts(trainer.id)
    
    stats_text = f"""
📊 <b>Статистика (из Supabase)</b>

<b>👥 Клиенты:</b>
• Всего: {clients_count}
• Активных: {clients_count}
• Новых за месяц: {clients_count}

<b>💪 Тренировки:</b>
• Проведено всего: {workouts_count}
• За этот месяц: {workouts_count}
• Сегодня: {len(today_workouts)}

<b>💰 Финансы:</b>
• Доход за месяц: - ₽
• Средний чек: - ₽

<b>☁️ База данных:</b>
• Провайдер: Supabase
• Статус: ✅ Подключена
• Проект: {supabase_config.SUPABASE_PROJECT_ID}

Для детальной аналитики и графиков откройте веб-приложение.
"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="📈 Детальная аналитика",
            web_app=WebAppInfo(url=f"{supabase_config.WEB_APP_URL}#/analytics")
        )
    )
    
    await message.answer(stats_text, reply_markup=keyboard.as_markup(), parse_mode="HTML")

# Обработка callback'ов
@main_router.callback_query(F.data == "profile")
async def callback_profile(callback):
    await callback.message.edit_reply_markup()
    await cmd_profile(callback.message)

@main_router.callback_query(F.data == "clients")
async def callback_clients(callback):
    await callback.message.edit_reply_markup()
    await cmd_clients(callback.message)

@main_router.callback_query(F.data == "workouts")
async def callback_workouts(callback):
    await callback.message.edit_reply_markup()
    await cmd_workouts(callback.message)

@main_router.callback_query(F.data == "stats")
async def callback_stats(callback):
    await callback.message.edit_reply_markup()
    await cmd_stats(callback.message)

# Регистрация роутеров (используем версии для Supabase)
from handlers.clients_supabase import clients_supabase_router
from handlers.workouts_supabase import workouts_supabase_router

dp.include_router(main_router)
dp.include_router(clients_supabase_router)
dp.include_router(workouts_supabase_router)

async def on_startup():
    """Действия при запуске бота с Supabase"""
    logger.info("🚀 Запуск фитнес-помощника (Supabase версия)...")
    
    # Инициализируем базу данных Supabase
    try:
        from shared.supabase_database import init_supabase_database
        await init_supabase_database()
        logger.info("✅ Supabase база данных инициализирована")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации Supabase: {e}")
        raise
    
    # Получаем информацию о боте
    try:
        bot_info = await bot.get_me()
        logger.info(f"🤖 Бот запущен успешно: @{bot_info.username}")
        logger.info(f"👤 Имя бота: {bot_info.first_name}")
        logger.info(f"🆔 ID бота: {bot_info.id}")
        logger.info(f"☁️ Supabase проект: {supabase_config.SUPABASE_PROJECT_ID}")
        
        # Устанавливаем команды
        from aiogram.types import BotCommand
        commands = [
            BotCommand(command="start", description="🏠 Главное меню"),
            BotCommand(command="help", description="❓ Помощь"),
            BotCommand(command="profile", description="👤 Профиль тренера"),
            BotCommand(command="clients", description="👥 Клиенты"),
            BotCommand(command="workouts", description="💪 Тренировки"),
            BotCommand(command="stats", description="📊 Статистика"),
        ]
        await bot.set_my_commands(commands)
        logger.info("✅ Команды бота установлены")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
        raise

async def on_shutdown():
    """Действия при остановке бота"""
    logger.info("🔄 Остановка бота...")
    
    # Закрываем соединение с Supabase
    try:
        from shared.supabase_database import supabase_db_manager
        await supabase_db_manager.close()
    except Exception as e:
        logger.error(f"❌ Ошибка при закрытии Supabase: {e}")
    
    await bot.session.close()
    logger.info("✅ Бот остановлен")

async def main():
    """Главная функция запуска бота с Supabase"""
    try:
        await on_startup()
        
        # Запуск бота
        logger.info("🏋️‍♂️ Фитнес-бот готов к работе с Supabase!")
        await dp.start_polling(bot, skip_updates=True)
        
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
    finally:
        await on_shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"💥 Неожиданная ошибка: {e}")
