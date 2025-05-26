from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from shared.supabase_database import SupabaseTrainerService, SupabaseClientService
from shared.models import Gender, Goal
from keyboards.main_menu import (
    get_clients_menu_keyboard, get_gender_keyboard, get_goal_keyboard, 
    get_activity_level_keyboard, get_client_actions_keyboard,
    get_confirmation_keyboard, get_pagination_keyboard
)
from utils.states import BotStates

clients_supabase_router = Router()

@clients_supabase_router.message(Command("clients"))
async def cmd_clients_supabase(message: Message):
    """Команда просмотра клиентов через Supabase"""
    await show_clients_list_supabase(message)

async def show_clients_list_supabase(message: Message):
    """Показать список клиентов из Supabase"""
    user_id = str(message.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    if not trainer:
        await message.answer("❌ Тренер не найден. Выполните /start для регистрации.")
        return
    
    clients = await SupabaseClientService.get_trainer_clients(trainer.id)
    
    if not clients:
        await message.answer(
            "📝 <b>У вас пока нет клиентов</b>\n\n"
            "Добавьте первого клиента, чтобы начать работу!\n\n"
            "☁️ <i>Все данные автоматически сохраняются в Supabase</i>",
            reply_markup=get_clients_menu_keyboard(),
            parse_mode="HTML"
        )
        return
    
    # Формируем список клиентов
    clients_text = f"👥 <b>Ваши клиенты ({len(clients)})</b>\n"
    clients_text += f"☁️ <i>Данные из Supabase</i>\n\n"
    
    for i, client in enumerate(clients[:10], 1):  # Показываем первых 10
        status = "✅" if client.is_active else "❌"
        goal_emoji = {
            Goal.WEIGHT_LOSS: "🔥",
            Goal.MUSCLE_GAIN: "💪", 
            Goal.STRENGTH: "⚡",
            Goal.ENDURANCE: "🏃‍♂️",
            Goal.HEALTH: "🏥",
            Goal.SPORT_SPECIFIC: "🏆"
        }.get(client.primary_goal, "🎯")
        
        clients_text += f"{i}. {status} <b>{client.first_name} {client.last_name or ''}</b>\n"
        clients_text += f"   {goal_emoji} {client.primary_goal.value if client.primary_goal else 'Цель не указана'}\n"
        if client.phone:
            clients_text += f"   📱 {client.phone}\n"
        clients_text += "\n"
    
    # Создаем клавиатуру с клиентами
    builder = InlineKeyboardBuilder()
    
    for client in clients[:10]:
        builder.row(
            InlineKeyboardButton(
                text=f"👤 {client.first_name} {client.last_name or ''}",
                callback_data=f"client_view_{client.id}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="➕ Добавить клиента", callback_data="client_add")
    )
    
    if len(clients) > 10:
        builder.row(
            InlineKeyboardButton(text="📋 Все клиенты", callback_data="client_list_all")
        )
    
    await message.answer(clients_text, reply_markup=builder.as_markup(), parse_mode="HTML")

@clients_supabase_router.callback_query(F.data == "client_list")
async def callback_clients_list_supabase(callback: CallbackQuery):
    """Обработка callback для списка клиентов из Supabase"""
    await callback.message.edit_reply_markup()
    await show_clients_list_supabase(callback.message)

@clients_supabase_router.callback_query(F.data == "client_add")
async def add_client_start_supabase(callback: CallbackQuery, state: FSMContext):
    """Начало добавления клиента в Supabase"""
    await callback.message.edit_text(
        "📝 <b>Добавление нового клиента</b>\n\n"
        "☁️ <i>Данные будут сохранены в Supabase</i>\n\n"
        "Введите имя клиента:",
        parse_mode="HTML"
    )
    await state.set_state(BotStates.CLIENT_FIRST_NAME)

@clients_supabase_router.message(BotStates.CLIENT_FIRST_NAME)
async def client_first_name_supabase(message: Message, state: FSMContext):
    """Ввод имени клиента для Supabase"""
    if len(message.text.strip()) < 2:
        await message.answer("❌ Имя должно содержать минимум 2 символа. Попробуйте еще раз:")
        return
    
    await state.update_data(first_name=message.text.strip())
    await message.answer("Введите фамилию клиента (или нажмите /skip для пропуска):")
    await state.set_state(BotStates.CLIENT_LAST_NAME)

@clients_supabase_router.message(BotStates.CLIENT_LAST_NAME)
async def client_last_name_supabase(message: Message, state: FSMContext):
    """Ввод фамилии клиента для Supabase"""
    last_name = None if message.text == "/skip" else message.text.strip()
    
    await state.update_data(last_name=last_name)
    await message.answer("Введите номер телефона клиента (или /skip):")
    await state.set_state(BotStates.CLIENT_PHONE)

@clients_supabase_router.message(BotStates.CLIENT_PHONE)
async def client_phone_supabase(message: Message, state: FSMContext):
    """Ввод телефона клиента для Supabase"""
    phone = None if message.text == "/skip" else message.text.strip()
    
    await state.update_data(phone=phone)
    await message.answer("Введите email клиента (или /skip):")
    await state.set_state(BotStates.CLIENT_EMAIL)

@clients_supabase_router.message(BotStates.CLIENT_EMAIL)
async def client_email_supabase(message: Message, state: FSMContext):
    """Ввод email клиента для Supabase"""
    email = None if message.text == "/skip" else message.text.strip()
    
    await state.update_data(email=email)
    await message.answer(
        "Выберите пол клиента:",
        reply_markup=get_gender_keyboard()
    )
    await state.set_state(BotStates.CLIENT_GENDER)

@clients_supabase_router.callback_query(F.data.startswith("gender_"), BotStates.CLIENT_GENDER)
async def client_gender_supabase(callback: CallbackQuery, state: FSMContext):
    """Выбор пола клиента для Supabase"""
    gender_map = {
        "gender_male": Gender.MALE,
        "gender_female": Gender.FEMALE,
        "gender_other": Gender.OTHER
    }
    
    gender = gender_map.get(callback.data)
    await state.update_data(gender=gender)
    
    await callback.message.edit_text(
        "Введите рост клиента в см (или /skip):",
    )
    await state.set_state(BotStates.CLIENT_HEIGHT)

@clients_supabase_router.message(BotStates.CLIENT_HEIGHT)
async def client_height_supabase(message: Message, state: FSMContext):
    """Ввод роста клиента для Supabase"""
    height = None
    
    if message.text != "/skip":
        try:
            height = float(message.text)
            if height < 100 or height > 250:
                await message.answer("❌ Рост должен быть от 100 до 250 см. Попробуйте еще раз:")
                return
        except ValueError:
            await message.answer("❌ Введите корректный рост в см:")
            return
    
    await state.update_data(height=height)
    await message.answer("Введите вес клиента в кг (или /skip):")
    await state.set_state(BotStates.CLIENT_WEIGHT)

@clients_supabase_router.message(BotStates.CLIENT_WEIGHT)
async def client_weight_supabase(message: Message, state: FSMContext):
    """Ввод веса клиента для Supabase"""
    weight = None
    
    if message.text != "/skip":
        try:
            weight = float(message.text)
            if weight < 30 or weight > 300:
                await message.answer("❌ Вес должен быть от 30 до 300 кг. Попробуйте еще раз:")
                return
        except ValueError:
            await message.answer("❌ Введите корректный вес в кг:")
            return
    
    await state.update_data(weight=weight)
    await message.answer(
        "Выберите основную цель клиента:",
        reply_markup=get_goal_keyboard()
    )
    await state.set_state(BotStates.CLIENT_GOAL)

@clients_supabase_router.callback_query(F.data.startswith("goal_"), BotStates.CLIENT_GOAL)
async def client_goal_supabase(callback: CallbackQuery, state: FSMContext):
    """Выбор цели клиента для Supabase"""
    goal_map = {
        "goal_weight_loss": Goal.WEIGHT_LOSS,
        "goal_muscle_gain": Goal.MUSCLE_GAIN,
        "goal_strength": Goal.STRENGTH,
        "goal_endurance": Goal.ENDURANCE,
        "goal_health": Goal.HEALTH,
        "goal_sport_specific": Goal.SPORT_SPECIFIC
    }
    
    goal = goal_map.get(callback.data)
    await state.update_data(primary_goal=goal)
    
    await callback.message.edit_text(
        "Выберите уровень активности клиента:",
        reply_markup=get_activity_level_keyboard()
    )
    await state.set_state(BotStates.CLIENT_ACTIVITY_LEVEL)

@clients_supabase_router.callback_query(F.data.startswith("activity_"), BotStates.CLIENT_ACTIVITY_LEVEL)
async def client_activity_level_supabase(callback: CallbackQuery, state: FSMContext):
    """Выбор уровня активности для Supabase"""
    activity_map = {
        "activity_sedentary": "sedentary",
        "activity_light": "light", 
        "activity_moderate": "moderate",
        "activity_active": "active",
        "activity_very_active": "very_active"
    }
    
    activity = activity_map.get(callback.data)
    await state.update_data(activity_level=activity)
    
    await callback.message.edit_text(
        "Введите медицинские противопоказания или особенности (или /skip):"
    )
    await state.set_state(BotStates.CLIENT_MEDICAL_CONDITIONS)

@clients_supabase_router.message(BotStates.CLIENT_MEDICAL_CONDITIONS)
async def client_medical_conditions_supabase(message: Message, state: FSMContext):
    """Ввод медицинских особенностей для Supabase"""
    medical = None if message.text == "/skip" else message.text.strip()
    
    # Получаем все данные
    data = await state.get_data()
    
    # Создаем клиента в Supabase
    user_id = str(message.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    client = await SupabaseClientService.create_client(
        trainer_id=trainer.id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        phone=data.get("phone"),
        email=data.get("email"),
        gender=data.get("gender"),
        height=data.get("height"),
        weight=data.get("weight"),
        primary_goal=data.get("primary_goal"),
        activity_level=data.get("activity_level"),
        medical_conditions=medical
    )
    
    # Формируем сводку
    summary_text = f"""
✅ <b>Клиент успешно добавлен в Supabase!</b>

👤 <b>{client.first_name} {client.last_name or ''}</b>
📱 {client.phone or 'Не указан'}
📧 {client.email or 'Не указан'}

📊 <b>Параметры:</b>
• Рост: {client.height or 'Не указан'} см
• Вес: {client.weight or 'Не указан'} кг
• Цель: {client.primary_goal.value if client.primary_goal else 'Не указана'}
• Активность: {client.activity_level or 'Не указана'}

☁️ <b>База данных:</b> Supabase
🆔 <b>ID клиента:</b> {client.id}

💡 <b>Что дальше?</b>
• Запланировать первую тренировку
• Создать программу тренировок
• Добавить план питания
"""
    
    await message.answer(
        summary_text,
        reply_markup=get_client_actions_keyboard(client.id),
        parse_mode="HTML"
    )
    await state.clear()

@clients_supabase_router.callback_query(F.data.startswith("client_view_"))
async def view_client_supabase(callback: CallbackQuery):
    """Просмотр информации о клиенте из Supabase"""
    client_id = int(callback.data.split("_")[2])
    
    client = await SupabaseClientService.get_client_by_id(client_id)
    
    if not client:
        await callback.message.edit_text("❌ Клиент не найден в Supabase")
        return
    
    # Получаем статистику тренировок из Supabase
    from shared.supabase_database import SupabaseWorkoutService
    workouts = await SupabaseWorkoutService.get_client_workouts(client_id, limit=5)
    total_workouts = len(await SupabaseWorkoutService.get_client_workouts(client_id))
    
    # Подсчитываем статистику
    completed_workouts = len([w for w in workouts if w.status.value == 'completed'])
    
    # Формируем детальную информацию
    client_text = f"""
👤 <b>{client.first_name} {client.last_name or ''}</b>
☁️ <i>Данные из Supabase (ID: {client.id})</i>

📱 <b>Контакты:</b>
• Телефон: {client.phone or 'Не указан'}
• Email: {client.email or 'Не указан'}

🔍 <b>Параметры:</b>
• Пол: {client.gender.value if client.gender else 'Не указан'}
• Рост: {client.height or 'Не указан'} см
• Вес: {client.weight or 'Не указан'} кг

🎯 <b>Цели:</b>
• Основная цель: {client.primary_goal.value if client.primary_goal else 'Не указана'}
• Целевой вес: {client.target_weight or 'Не указан'} кг
• Уровень активности: {client.activity_level or 'Не указан'}

💪 <b>Статистика тренировок:</b>
• Всего: {total_workouts}
• Завершено: {completed_workouts}
• Посещаемость: {(completed_workouts/total_workouts*100) if total_workouts > 0 else 0:.0f}%
"""
    
    if workouts:
        client_text += "\n📅 <b>Последние тренировки:</b>\n"
        for workout in workouts[:3]:
            status_emoji = {
                "planned": "⏳",
                "completed": "✅", 
                "missed": "❌",
                "cancelled": "🚫"
            }
            emoji = status_emoji.get(workout.status.value, "⏳")
            date_str = workout.scheduled_date.strftime("%d.%m.%Y %H:%M")
            
            # Извлекаем тип тренировки из заметок
            workout_type = ""
            if workout.trainer_notes and workout.trainer_notes.startswith('['):
                end_bracket = workout.trainer_notes.find(']')
                if end_bracket > 0:
                    workout_type = workout.trainer_notes[1:end_bracket]
            
            client_text += f"{emoji} {date_str} - {workout_type}\n"
    
    if client.medical_conditions:
        client_text += f"\n🏥 <b>Медицинские особенности:</b>\n{client.medical_conditions}"
    
    if client.injuries:
        client_text += f"\n🩹 <b>Травмы:</b>\n{client.injuries}"
    
    # Добавляем дату регистрации
    client_text += f"\n\n📅 <b>Регистрация:</b> {client.created_at.strftime('%d.%m.%Y')}"
    
    # Создаем клавиатуру с опциями
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💪 Создать тренировку", callback_data=f"workout_create_for_{client_id}")
    )
    builder.row(
        InlineKeyboardButton(text="📅 История тренировок", callback_data=f"client_workout_history_{client_id}"),
        InlineKeyboardButton(text="📈 Прогресс", callback_data=f"client_progress_{client_id}")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Замеры", callback_data=f"client_measurements_{client_id}"),
        InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"client_edit_{client_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data=f"client_view_{client_id}"),
        InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"client_delete_{client_id}")
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="client_list")
    )
    
    await callback.message.edit_text(
        client_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@clients_supabase_router.callback_query(F.data.startswith("client_delete_"))
async def delete_client_confirm_supabase(callback: CallbackQuery):
    """Подтверждение удаления клиента из Supabase"""
    client_id = int(callback.data.split("_")[2])
    
    client = await SupabaseClientService.get_client_by_id(client_id)
    if not client:
        await callback.message.edit_text("❌ Клиент не найден в Supabase")
        return
    
    await callback.message.edit_text(
        f"⚠️ <b>Подтверждение удаления</b>\n\n"
        f"Вы действительно хотите удалить клиента из Supabase?\n"
        f"<b>{client.first_name} {client.last_name or ''}</b>\n\n"
        "⚠️ Это действие нельзя отменить!\n"
        "☁️ Данные будут удалены из облачной базы данных",
        reply_markup=get_confirmation_keyboard("delete_client", client_id),
        parse_mode="HTML"
    )

@clients_supabase_router.callback_query(F.data.startswith("confirm_delete_client_"))
async def delete_client_confirmed_supabase(callback: CallbackQuery):
    """Подтвержденное удаление клиента из Supabase"""
    client_id = int(callback.data.split("_")[3])
    
    client = await SupabaseClientService.get_client_by_id(client_id)
    if client:
        client_name = f"{client.first_name} {client.last_name or ''}"
        await SupabaseClientService.delete_client(client_id)
        
        await callback.message.edit_text(
            f"✅ <b>Клиент удален</b>\n\n"
            f"{client_name} успешно удален из Supabase.\n\n"
            "☁️ Данные удалены из облачной базы данных",
            parse_mode="HTML"
        )
        
        # Показываем список клиентов через 3 секунды
        import asyncio
        await asyncio.sleep(2)
        await show_clients_list_supabase(callback.message)
    else:
        await callback.message.edit_text("❌ Клиент не найден в Supabase")

@clients_supabase_router.callback_query(F.data.startswith("cancel_delete_client_"))
async def delete_client_cancelled_supabase(callback: CallbackQuery):
    """Отмена удаления клиента"""
    client_id = int(callback.data.split("_")[3])
    
    # Возвращаемся к просмотру клиента
    await view_client_supabase(callback)

@clients_supabase_router.callback_query(F.data == "client_search")
async def search_client_start_supabase(callback: CallbackQuery, state: FSMContext):
    """Начало поиска клиентов в Supabase"""
    await callback.message.edit_text(
        "🔍 <b>Поиск клиентов</b>\n\n"
        "☁️ <i>Поиск по базе данных Supabase</i>\n\n"
        "Введите часть имени или фамилии клиента:",
        parse_mode="HTML"
    )
    await state.set_state(BotStates.CLIENT_SEARCH)

@clients_supabase_router.message(BotStates.CLIENT_SEARCH)
async def search_client_query_supabase(message: Message, state: FSMContext):
    """Обработка запроса поиска в Supabase"""
    user_id = str(message.from_user.id)
    trainer = await SupabaseTrainerService.get_trainer_by_telegram_id(user_id)
    
    if not trainer:
        await message.answer("❌ Тренер не найден")
        await state.clear()
        return
    
    query = message.text.strip()
    
    if len(query) < 2:
        await message.answer("❌ Запрос должен содержать минимум 2 символа. Попробуйте еще раз:")
        return
    
    # Поиск клиентов в Supabase
    clients = await SupabaseClientService.search_clients(trainer.id, query)
    
    if not clients:
        await message.answer(
            f"🔍 <b>Поиск: \"{query}\"</b>\n\n"
            "Клиенты не найдены в Supabase.",
            parse_mode="HTML"
        )
        await state.clear()
        return
    
    # Формируем результаты поиска
    search_text = f"🔍 <b>Поиск: \"{query}\"</b>\n"
    search_text += f"☁️ <i>Результаты из Supabase</i>\n\n"
    search_text += f"Найдено клиентов: {len(clients)}\n\n"
    
    builder = InlineKeyboardBuilder()
    
    for client in clients:
        status = "✅" if client.is_active else "❌"
        goal_emoji = {
            Goal.WEIGHT_LOSS: "🔥",
            Goal.MUSCLE_GAIN: "💪", 
            Goal.STRENGTH: "⚡",
            Goal.ENDURANCE: "🏃‍♂️",
            Goal.HEALTH: "🏥",
            Goal.SPORT_SPECIFIC: "🏆"
        }.get(client.primary_goal, "🎯")
        
        search_text += f"{status} <b>{client.first_name} {client.last_name or ''}</b>\n"
        search_text += f"   {goal_emoji} {client.primary_goal.value if client.primary_goal else 'Цель не указана'}\n"
        if client.phone:
            search_text += f"   📱 {client.phone}\n"
        search_text += f"   🆔 ID: {client.id}\n\n"
        
        builder.row(
            InlineKeyboardButton(
                text=f"👤 {client.first_name} {client.last_name or ''}",
                callback_data=f"client_view_{client.id}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="🔍 Новый поиск", callback_data="client_search")
    )
    
    await message.answer(
        search_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await state.clear()
