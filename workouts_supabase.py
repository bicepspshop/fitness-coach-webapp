from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from shared.supabase_database import SupabaseTrainerService, SupabaseClientService, SupabaseWorkoutService
from shared.models import WorkoutStatus
from keyboards.main_menu import (
    get_workouts_menu_keyboard, get_workout_type_keyboard, 
    get_confirmation_keyboard
)
from utils.states import BotStates
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

workouts_supabase_router = Router()

@workouts_supabase_router.message(Command("workouts"))
async def cmd_workouts_supabase(message: Message):
    """Команда управления тренировками через Supabase"""
    await show_workouts_menu_supabase(message)

async def show_workouts_menu_supabase(message: Message):
    """Показать меню тренировок из Supabase"""
    user_id = str(message.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    if not trainer:
        await message.answer("❌ Тренер не найден. Выполните /start для регистрации.")
        return
    
    # Получаем статистику из Supabase
    total_workouts = await SupabaseWorkoutService.get_workouts_count(trainer.id)
    today_workouts = await SupabaseWorkoutService.get_today_workouts(trainer.id)
    upcoming_workouts = await SupabaseWorkoutService.get_upcoming_workouts(trainer.id, limit=5)
    
    workouts_text = f"""
💪 <b>Управление тренировками</b>
☁️ <i>Данные из Supabase</i>

📊 <b>Статистика:</b>
• Всего тренировок: {total_workouts}
• Сегодня: {len(today_workouts)}
• Ближайших: {len(upcoming_workouts)}

📅 <b>На сегодня:</b>
"""
    
    if today_workouts:
        for workout in today_workouts:
            time_str = workout.scheduled_date.strftime('%H:%M')
            status_emoji = {
                "planned": "⏳",
                "completed": "✅", 
                "missed": "❌",
                "cancelled": "🚫"
            }
            emoji = status_emoji.get(workout.status.value, "⏳")
            
            # Извлекаем тип тренировки
            workout_type = "Тренировка"
            if workout.trainer_notes and workout.trainer_notes.startswith('['):
                end_bracket = workout.trainer_notes.find(']')
                if end_bracket > 0:
                    workout_type = workout.trainer_notes[1:end_bracket]
            
            workouts_text += f"• {emoji} {time_str} - {workout.client.first_name} ({workout_type})\n"
    else:
        workouts_text += "Нет запланированных тренировок\n"
    
    workouts_text += f"""
🔧 <b>Возможности:</b>
• ➕ Создать новую тренировку
• 📅 Просмотр расписания
• 📊 Статистика и отчеты
• ⏰ Напоминания клиентам

Все тренировки автоматически сохраняются в Supabase.
"""
    
    # Создаем клавиатуру
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕ Создать тренировку", callback_data="workout_add")
    )
    builder.row(
        InlineKeyboardButton(text="📅 На сегодня", callback_data="workout_today"),
        InlineKeyboardButton(text="📊 Все тренировки", callback_data="workout_all")
    )
    builder.row(
        InlineKeyboardButton(text="🔍 Поиск", callback_data="workout_search"),
        InlineKeyboardButton(text="📈 Статистика", callback_data="workout_stats")
    )
    
    await message.answer(workouts_text, reply_markup=builder.as_markup(), parse_mode="HTML")

@workouts_supabase_router.callback_query(F.data == "workout_add")
async def add_workout_start_supabase(callback: CallbackQuery, state: FSMContext):
    """Начало создания тренировки в Supabase"""
    user_id = str(callback.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    if not trainer:
        await callback.message.edit_text("❌ Тренер не найден")
        return
    
    # Получаем список клиентов
    clients = await SupabaseClientService.get_trainer_clients(trainer.id)
    
    if not clients:
        await callback.message.edit_text(
            "❌ <b>У вас нет клиентов</b>\n\n"
            "Сначала добавьте клиентов для планирования тренировок.\n\n"
            "☁️ Используйте команду /clients",
            parse_mode="HTML"
        )
        return
    
    # Сохраняем ID тренера
    await state.update_data(trainer_id=trainer.id)
    
    # Показываем список клиентов
    clients_text = "👥 <b>Выберите клиента для тренировки:</b>\n\n"
    
    builder = InlineKeyboardBuilder()
    
    for client in clients:
        clients_text += f"• {client.first_name} {client.last_name or ''}\n"
        builder.row(
            InlineKeyboardButton(
                text=f"👤 {client.first_name} {client.last_name or ''}",
                callback_data=f"workout_select_client_{client.id}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="workout_menu")
    )
    
    await callback.message.edit_text(clients_text, reply_markup=builder.as_markup(), parse_mode="HTML")

@workouts_supabase_router.callback_query(F.data.startswith("workout_select_client_"))
async def select_client_for_workout_supabase(callback: CallbackQuery, state: FSMContext):
    """Выбор клиента для тренировки в Supabase"""
    client_id = int(callback.data.split("_")[3])
    
    client = await SupabaseClientService.get_client_by_id(client_id)
    if not client:
        await callback.message.edit_text("❌ Клиент не найден")
        return
    
    # Сохраняем ID клиента
    await state.update_data(client_id=client_id)
    
    await callback.message.edit_text(
        f"📅 <b>Тренировка для: {client.first_name} {client.last_name or ''}</b>\n\n"
        "Введите дату и время тренировки.\n\n"
        "<b>Примеры:</b>\n"
        "• <code>сегодня 18:00</code>\n"
        "• <code>завтра 10:30</code>\n"
        "• <code>28.05.2024 15:00</code>\n"
        "• <code>понедельник 09:00</code>",
        parse_mode="HTML"
    )
    await state.set_state(BotStates.WORKOUT_DATETIME)

@workouts_supabase_router.message(BotStates.WORKOUT_DATETIME)
async def workout_datetime_supabase(message: Message, state: FSMContext):
    """Ввод даты и времени тренировки для Supabase"""
    try:
        # Парсим дату и время
        scheduled_date = parse_datetime_string(message.text.strip())
        
        if not scheduled_date:
            await message.answer(
                "❌ Не удалось распознать дату и время.\n\n"
                "Попробуйте еще раз, например:\n"
                "• сегодня 18:00\n"
                "• завтра 15:30\n"
                "• 30.05.2024 10:00"
            )
            return
        
        # Проверяем, что дата не в прошлом
        if scheduled_date < datetime.now():
            await message.answer("❌ Нельзя планировать тренировку в прошлом. Введите будущую дату:")
            return
        
        await state.update_data(scheduled_date=scheduled_date)
        
        # Показываем типы тренировок
        await message.answer(
            f"📅 <b>Дата:</b> {scheduled_date.strftime('%d.%m.%Y %H:%M')}\n\n"
            "Выберите тип тренировки:",
            reply_markup=get_workout_type_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(BotStates.WORKOUT_TYPE)
        
    except Exception as e:
        logger.error(f"Ошибка парсинга даты: {e}")
        await message.answer(
            "❌ Ошибка при обработке даты. Попробуйте еще раз.\n\n"
            "Примеры правильного формата:\n"
            "• сегодня 18:00\n"
            "• завтра 15:30\n"
            "• 30.05.2024 10:00"
        )

@workouts_supabase_router.callback_query(F.data.startswith("workout_type_"), BotStates.WORKOUT_TYPE)
async def workout_type_supabase(callback: CallbackQuery, state: FSMContext):
    """Выбор типа тренировки для Supabase"""
    workout_type_map = {
        "workout_type_strength": "Силовая",
        "workout_type_cardio": "Кардио",
        "workout_type_functional": "Функциональная",
        "workout_type_stretching": "Растяжка",
        "workout_type_martial_arts": "Единоборства",
        "workout_type_swimming": "Плавание",
        "workout_type_cycling": "Велосипед",
        "workout_type_mixed": "Смешанная"
    }
    
    workout_type = workout_type_map.get(callback.data, "Тренировка")
    await state.update_data(workout_type=workout_type)
    
    await callback.message.edit_text(
        f"🏋️ <b>Тип тренировки:</b> {workout_type}\n\n"
        "Введите длительность тренировки в минутах (или нажмите /skip для 60 минут):"
    )
    await state.set_state(BotStates.WORKOUT_DURATION)

@workouts_supabase_router.message(BotStates.WORKOUT_DURATION)
async def workout_duration_supabase(message: Message, state: FSMContext):
    """Ввод длительности тренировки для Supabase"""
    duration = 60  # По умолчанию 60 минут
    
    if message.text != "/skip":
        try:
            duration = int(message.text)
            if duration < 15 or duration > 300:
                await message.answer("❌ Длительность должна быть от 15 до 300 минут. Попробуйте еще раз:")
                return
        except ValueError:
            await message.answer("❌ Введите число (количество минут):")
            return
    
    await state.update_data(duration_minutes=duration)
    
    await message.answer(
        f"⏱️ <b>Длительность:</b> {duration} минут\n\n"
        "Введите место проведения тренировки (или /skip):"
    )
    await state.set_state(BotStates.WORKOUT_LOCATION)

@workouts_supabase_router.message(BotStates.WORKOUT_LOCATION)
async def workout_location_supabase(message: Message, state: FSMContext):
    """Ввод места тренировки для Supabase"""
    location = None if message.text == "/skip" else message.text.strip()
    
    await state.update_data(location=location)
    
    await message.answer(
        "📝 Введите заметки к тренировке (или /skip):"
    )
    await state.set_state(BotStates.WORKOUT_NOTES)

@workouts_supabase_router.message(BotStates.WORKOUT_NOTES)
async def workout_notes_supabase(message: Message, state: FSMContext):
    """Ввод заметок и создание тренировки в Supabase"""
    notes = None if message.text == "/skip" else message.text.strip()
    
    # Получаем все данные
    data = await state.get_data()
    
    try:
        # Создаем тренировку в Supabase
        workout = await SupabaseWorkoutService.create_workout(
            trainer_id=data.get("trainer_id"),
            client_id=data.get("client_id"),
            scheduled_date=data.get("scheduled_date"),
            workout_type=data.get("workout_type"),
            duration_minutes=data.get("duration_minutes"),
            location=data.get("location"),
            trainer_notes=notes
        )
        
        # Получаем информацию о клиенте
        client = await SupabaseClientService.get_client_by_id(data.get("client_id"))
        
        # Формируем сводку
        summary_text = f"""
✅ <b>Тренировка создана в Supabase!</b>

👤 <b>Клиент:</b> {client.first_name} {client.last_name or ''}
📅 <b>Дата:</b> {workout.scheduled_date.strftime('%d.%m.%Y %H:%M')}
🏋️ <b>Тип:</b> {data.get("workout_type")}
⏱️ <b>Длительность:</b> {workout.duration_minutes} минут
📍 <b>Место:</b> {workout.location or 'Не указано'}

☁️ <b>ID тренировки:</b> {workout.id}
📊 <b>Статус:</b> ⏳ Запланирована

💡 <b>Что дальше?</b>
• Добавить план упражнений
• Отправить уведомление клиенту
• Посмотреть расписание
"""
        
        # Создаем клавиатуру с действиями
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="📋 Добавить упражнения", callback_data=f"workout_add_exercises_{workout.id}")
        )
        builder.row(
            InlineKeyboardButton(text="📅 Расписание", callback_data="workout_today"),
            InlineKeyboardButton(text="💪 Новая тренировка", callback_data="workout_add")
        )
        
        await message.answer(
            summary_text,
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"Ошибка создания тренировки в Supabase: {e}")
        await message.answer(
            "❌ Ошибка при создании тренировки в Supabase.\n"
            "Попробуйте еще раз или обратитесь к администратору."
        )
    
    await state.clear()

@workouts_supabase_router.callback_query(F.data == "workout_today")
async def show_today_workouts_supabase(callback: CallbackQuery):
    """Показать тренировки на сегодня из Supabase"""
    user_id = str(callback.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    if not trainer:
        await callback.message.edit_text("❌ Тренер не найден")
        return
    
    today_workouts = await SupabaseWorkoutService.get_today_workouts(trainer.id)
    
    if not today_workouts:
        await callback.message.edit_text(
            "📅 <b>Тренировки на сегодня</b>\n\n"
            "Сегодня нет запланированных тренировок.\n\n"
            "☁️ <i>Данные из Supabase</i>",
            parse_mode="HTML"
        )
        return
    
    workouts_text = f"📅 <b>Тренировки на сегодня ({len(today_workouts)})</b>\n"
    workouts_text += f"☁️ <i>Данные из Supabase</i>\n\n"
    
    builder = InlineKeyboardBuilder()
    
    for workout in today_workouts:
        time_str = workout.scheduled_date.strftime('%H:%M')
        
        status_emoji = {
            "planned": "⏳",
            "completed": "✅", 
            "missed": "❌",
            "cancelled": "🚫"
        }
        emoji = status_emoji.get(workout.status.value, "⏳")
        
        # Извлекаем тип тренировки
        workout_type = "Тренировка"
        if workout.trainer_notes and workout.trainer_notes.startswith('['):
            end_bracket = workout.trainer_notes.find(']')
            if end_bracket > 0:
                workout_type = workout.trainer_notes[1:end_bracket]
        
        workouts_text += f"{emoji} <b>{time_str}</b> - {workout.client.first_name} {workout.client.last_name or ''}\n"
        workouts_text += f"   🏋️ {workout_type} ({workout.duration_minutes} мин)\n"
        if workout.location:
            workouts_text += f"   📍 {workout.location}\n"
        workouts_text += f"   🆔 ID: {workout.id}\n\n"
        
        builder.row(
            InlineKeyboardButton(
                text=f"{time_str} - {workout.client.first_name}",
                callback_data=f"workout_view_{workout.id}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="➕ Новая тренировка", callback_data="workout_add")
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="workout_menu")
    )
    
    await callback.message.edit_text(
        workouts_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@workouts_supabase_router.callback_query(F.data.startswith("workout_view_"))
async def view_workout_supabase(callback: CallbackQuery):
    """Просмотр детали тренировки из Supabase"""
    workout_id = int(callback.data.split("_")[2])
    
    workout = await SupabaseWorkoutService.get_workout_by_id(workout_id)
    
    if not workout:
        await callback.message.edit_text("❌ Тренировка не найдена в Supabase")
        return
    
    # Формируем детальную информацию
    status_names = {
        "planned": "⏳ Запланирована",
        "completed": "✅ Завершена",
        "missed": "❌ Пропущена", 
        "cancelled": "🚫 Отменена"
    }
    
    status_name = status_names.get(workout.status.value, workout.status.value)
    date_str = workout.scheduled_date.strftime("%d.%m.%Y %H:%M")
    
    # Извлекаем тип тренировки
    workout_type = "Тренировка"
    notes = workout.trainer_notes or ""
    if notes.startswith('['):
        end_bracket = notes.find(']')
        if end_bracket > 0:
            workout_type = notes[1:end_bracket]
            notes = notes[end_bracket+1:].strip()
    
    workout_text = f"""
💪 <b>Детали тренировки</b>
☁️ <i>Данные из Supabase (ID: {workout.id})</i>

👤 <b>Клиент:</b> {workout.client.first_name} {workout.client.last_name or ''}
📅 <b>Дата:</b> {date_str}
🏋️ <b>Тип:</b> {workout_type}
🕐 <b>Длительность:</b> {workout.duration_minutes or 60} минут
📍 <b>Место:</b> {workout.location or 'Не указано'}
🎯 <b>Статус:</b> {status_name}
"""
    
    if workout.completed_at:
        completed_str = workout.completed_at.strftime("%d.%m.%Y %H:%M")
        workout_text += f"✅ <b>Завершена:</b> {completed_str}\n"
    
    if notes:
        workout_text += f"\n📝 <b>Заметки тренера:</b>\n{notes}"
    
    # Если есть план упражнений
    if workout.exercises:
        workout_text += "\n\n🏋️‍♀️ <b>План упражнений:</b>\n"
        for i, exercise in enumerate(workout.exercises, 1):
            exercise_name = exercise.get('name', 'Упражнение')
            sets = exercise.get('sets', 1)
            reps = exercise.get('reps', '')
            weight = exercise.get('weight', '')
            
            exercise_line = f"{i}. {exercise_name}"
            if sets:
                exercise_line += f" - {sets} подходов"
            if reps:
                exercise_line += f" x {reps}"
            if weight:
                exercise_line += f" ({weight} кг)"
            
            workout_text += exercise_line + "\n"
    
    if workout.client_feedback:
        workout_text += f"\n💬 <b>Отзыв клиента:</b>\n{workout.client_feedback}"
    
    if workout.perceived_exertion:
        workout_text += f"\n💪 <b>Усилие (1-10):</b> {workout.perceived_exertion}/10"
    
    # Создаем клавиатуру действий
    builder = InlineKeyboardBuilder()
    
    if workout.status.value == 'planned':
        builder.row(
            InlineKeyboardButton(text="📝 Изменить план", callback_data=f"workout_edit_plan_{workout_id}"),
            InlineKeyboardButton(text="✅ Отметить выполненной", callback_data=f"workout_complete_{workout_id}")
        )
        builder.row(
            InlineKeyboardButton(text="🚫 Отменить", callback_data=f"workout_cancel_{workout_id}")
        )
    elif workout.status.value == 'completed':
        builder.row(
            InlineKeyboardButton(text="📊 Добавить отчет", callback_data=f"workout_add_report_{workout_id}")
        )
    
    builder.row(
        InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"workout_delete_confirm_{workout_id}"),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="workout_today")
    )
    
    await callback.message.edit_text(
        workout_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@workouts_supabase_router.callback_query(F.data.startswith("workout_complete_"))
async def complete_workout_supabase(callback: CallbackQuery):
    """Отметить тренировку как завершенную в Supabase"""
    workout_id = int(callback.data.split("_")[2])
    
    try:
        await SupabaseWorkoutService.update_workout_status(
            workout_id, 
            'completed'
        )
        
        await callback.message.edit_text(
            "✅ <b>Тренировка отмечена как завершенная!</b>\n\n"
            "☁️ Статус обновлен в Supabase.\n\n"
            "Хотите добавить отчет о тренировке?",
            parse_mode="HTML"
        )
        
        # Показываем кнопки для дальнейших действий
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="📊 Добавить отчет", callback_data=f"workout_add_report_{workout_id}")
        )
        builder.row(
            InlineKeyboardButton(text="📅 К расписанию", callback_data="workout_today"),
            InlineKeyboardButton(text="💪 Новая тренировка", callback_data="workout_add")
        )
        
        await callback.message.edit_reply_markup(reply_markup=builder.as_markup())
        
    except Exception as e:
        logger.error(f"Ошибка обновления статуса тренировки в Supabase: {e}")
        await callback.answer("❌ Ошибка при обновлении статуса в Supabase")

@workouts_supabase_router.callback_query(F.data.startswith("workout_delete_confirm_"))
async def delete_workout_confirm_supabase(callback: CallbackQuery):
    """Подтверждение удаления тренировки из Supabase"""
    workout_id = int(callback.data.split("_")[3])
    
    workout = await SupabaseWorkoutService.get_workout_by_id(workout_id)
    if not workout:
        await callback.message.edit_text("❌ Тренировка не найдена в Supabase")
        return
    
    date_str = workout.scheduled_date.strftime("%d.%m.%Y %H:%M")
    
    await callback.message.edit_text(
        f"⚠️ <b>Подтверждение удаления</b>\n\n"
        f"Удалить тренировку из Supabase?\n\n"
        f"📅 <b>Дата:</b> {date_str}\n"
        f"👤 <b>Клиент:</b> {workout.client.first_name} {workout.client.last_name or ''}\n\n"
        "⚠️ Это действие нельзя отменить!\n"
        "☁️ Данные будут удалены из облачной базы данных",
        reply_markup=get_confirmation_keyboard("delete_workout", workout_id),
        parse_mode="HTML"
    )

@workouts_supabase_router.callback_query(F.data.startswith("confirm_delete_workout_"))
async def delete_workout_confirmed_supabase(callback: CallbackQuery):
    """Подтвержденное удаление тренировки из Supabase"""
    workout_id = int(callback.data.split("_")[3])
    
    try:
        await SupabaseWorkoutService.delete_workout(workout_id)
        
        await callback.message.edit_text(
            f"✅ <b>Тренировка удалена</b>\n\n"
            f"Тренировка успешно удалена из Supabase.\n\n"
            "☁️ Данные удалены из облачной базы данных",
            parse_mode="HTML"
        )
        
        # Показываем меню тренировок через 2 секунды
        import asyncio
        await asyncio.sleep(2)
        await show_workouts_menu_supabase(callback.message)
        
    except Exception as e:
        logger.error(f"Ошибка удаления тренировки из Supabase: {e}")
        await callback.answer("❌ Ошибка при удалении тренировки из Supabase")

def parse_datetime_string(text: str) -> datetime:
    """Парсинг строки даты и времени"""
    from datetime import datetime, timedelta
    import re
    
    text = text.lower().strip()
    now = datetime.now()
    
    # Регулярные выражения для разных форматов
    time_pattern = r'(\d{1,2}):(\d{2})'
    date_pattern = r'(\d{1,2})\.(\d{1,2})\.(\d{4})'
    
    # Извлекаем время
    time_match = re.search(time_pattern, text)
    if not time_match:
        return None
    
    hour = int(time_match.group(1))
    minute = int(time_match.group(2))
    
    if hour > 23 or minute > 59:
        return None
    
    # Определяем дату
    if 'сегодня' in text:
        target_date = now.date()
    elif 'завтра' in text:
        target_date = (now + timedelta(days=1)).date()
    elif 'понедельник' in text:
        days_ahead = 0 - now.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        target_date = (now + timedelta(days=days_ahead)).date()
    elif 'вторник' in text:
        days_ahead = 1 - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        target_date = (now + timedelta(days=days_ahead)).date()
    elif 'среда' in text or 'среду' in text:
        days_ahead = 2 - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        target_date = (now + timedelta(days=days_ahead)).date()
    elif 'четверг' in text:
        days_ahead = 3 - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        target_date = (now + timedelta(days=days_ahead)).date()
    elif 'пятниц' in text:
        days_ahead = 4 - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        target_date = (now + timedelta(days=days_ahead)).date()
    elif 'суббот' in text:
        days_ahead = 5 - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        target_date = (now + timedelta(days=days_ahead)).date()
    elif 'воскресень' in text:
        days_ahead = 6 - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        target_date = (now + timedelta(days=days_ahead)).date()
    else:
        # Пытаемся найти дату в формате дд.мм.гггг
        date_match = re.search(date_pattern, text)
        if date_match:
            day = int(date_match.group(1))
            month = int(date_match.group(2))
            year = int(date_match.group(3))
            try:
                target_date = datetime(year, month, day).date()
            except ValueError:
                return None
        else:
            return None
    
    # Создаем datetime объект
    try:
        result = datetime.combine(target_date, datetime.min.time().replace(hour=hour, minute=minute))
        return result
    except ValueError:
        return None
