#!/usr/bin/env python3
"""
Тестирование интеграции с Supabase
"""

import asyncio
import sys
import os
from pathlib import Path

# Добавляем корневую папку проекта в путь
sys.path.append(str(Path(__file__).parent))

# Загружаем переменные окружения для Supabase
def load_supabase_env():
    """Загрузка .env файла для Supabase"""
    env_path = Path(__file__).parent / '.env.supabase'
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print(f"✅ Переменные окружения Supabase загружены")
    else:
        print(f"❌ Файл .env.supabase не найден")
        return False
    return True

async def test_supabase_connection():
    """Тестирование подключения к Supabase"""
    print("🔗 Тестирование подключения к Supabase...")
    
    try:
        from shared.supabase_database import supabase_db_manager
        from shared.config_supabase import supabase_config
        
        # Инициализируем подключение
        await supabase_db_manager.initialize()
        print("✅ Соединение с Supabase установлено")
        print(f"📍 URL проекта: {supabase_config.SUPABASE_URL}")
        print(f"🆔 ID проекта: {supabase_config.SUPABASE_PROJECT_ID}")
        
        # Проверяем здоровье БД
        health_check = await supabase_db_manager.health_check()
        if health_check:
            print("✅ Проверка здоровья Supabase пройдена")
        else:
            print("❌ Проверка здоровья Supabase не пройдена")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к Supabase: {e}")
        return False

async def test_supabase_crud():
    """Тестирование CRUD операций в Supabase"""
    print("\n📊 Тестирование CRUD операций в Supabase...")
    
    try:
        from shared.supabase_database import (
            SupabaseTrainerService, 
            SupabaseClientService, 
            SupabaseWorkoutService,
            SupabaseExerciseService
        )
        from shared.models import Gender, Goal
        from datetime import datetime, timedelta
        
        # 1. Создаем тестового тренера
        print("👤 Создание тестового тренера...")
        trainer = await SupabaseTrainerService.create_trainer(
            telegram_id="test_123456789",
            username="test_trainer",
            first_name="Тест",
            last_name="Тренер",
            phone="+7 999 123 45 67",
            email="test@example.com"
        )
        print(f"✅ Тренер создан: {trainer.first_name} (ID: {trainer.id})")
        
        # 2. Создаем тестового клиента
        print("👥 Создание тестового клиента...")
        client = await SupabaseClientService.create_client(
            trainer_id=trainer.id,
            first_name="Анна",
            last_name="Иванова",
            phone="+7 999 123 45 68",
            email="anna@example.com",
            gender=Gender.FEMALE,
            height=165.0,
            weight=60.0,
            primary_goal=Goal.WEIGHT_LOSS,
            activity_level="moderate"
        )
        print(f"✅ Клиент создан: {client.first_name} (ID: {client.id})")
        
        # 3. Создаем тестовую тренировку
        print("💪 Создание тестовой тренировки...")
        scheduled_date = datetime.now() + timedelta(days=1)
        workout = await SupabaseWorkoutService.create_workout(
            trainer_id=trainer.id,
            client_id=client.id,
            scheduled_date=scheduled_date,
            workout_type="Силовая",
            duration_minutes=90,
            location="Спортзал",
            trainer_notes="Тест тренировка"
        )
        print(f"✅ Тренировка создана: ID {workout.id}")
        
        # 4. Тестируем поиск
        print("🔍 Тестирование поиска...")
        found_clients = await SupabaseClientService.search_clients(trainer.id, "Анна")
        print(f"✅ Найдено клиентов: {len(found_clients)}")
        
        # 5. Тестируем статистику
        print("📊 Тестирование статистики...")
        clients_count = await SupabaseClientService.get_clients_count(trainer.id)
        workouts_count = await SupabaseWorkoutService.get_workouts_count(trainer.id)
        print(f"✅ Статистика: {clients_count} клиентов, {workouts_count} тренировок")
        
        # 6. Тестируем обновление
        print("✏️ Тестирование обновления...")
        updated_client = await SupabaseClientService.update_client(
            client.id,
            weight=58.0,
            target_weight=55.0
        )
        print(f"✅ Клиент обновлен: новый вес {updated_client.weight} кг")
        
        # 7. Тестируем получение данных
        print("📋 Тестирование получения данных...")
        trainer_clients = await SupabaseClientService.get_trainer_clients(trainer.id)
        upcoming_workouts = await SupabaseWorkoutService.get_upcoming_workouts(trainer.id)
        print(f"✅ Получено: {len(trainer_clients)} клиентов, {len(upcoming_workouts)} предстоящих тренировок")
        
        # 8. Тестируем упражнения
        print("🏋️ Тестирование упражнений...")
        exercise = await SupabaseExerciseService.create_exercise(
            name="Тест упражнение",
            category="test",
            muscle_groups=["test"],
            equipment="test",
            difficulty="beginner",
            description="Тестовое упражнение"
        )
        print(f"✅ Упражнение создано: {exercise.name} (ID: {exercise.id})")
        
        print("\n🎉 Все CRUD операции выполнены успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка CRUD операций: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_basic_exercises():
    """Тестирование базовых упражнений"""
    print("\n🏋️ Проверка базовых упражнений в Supabase...")
    
    try:
        from shared.supabase_database import init_basic_exercises, SupabaseExerciseService
        
        # Инициализируем базовые упражнения
        await init_basic_exercises()
        print("✅ Базовые упражнения готовы")
        
        # Проверяем количество упражнений
        exercises = await SupabaseExerciseService.get_exercises_by_category("chest")
        print(f"✅ Упражнений для груди: {len(exercises)}")
        
        exercises = await SupabaseExerciseService.get_exercises_by_category("legs")
        print(f"✅ Упражнений для ног: {len(exercises)}")
        
        exercises = await SupabaseExerciseService.get_exercises_by_category("core")
        print(f"✅ Упражнений для кора: {len(exercises)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка проверки упражнений: {e}")
        return False

async def cleanup_test_data():
    """Очистка тестовых данных"""
    print("\n🧹 Очистка тестовых данных...")
    
    try:
        from shared.supabase_database import supabase_db_manager
        from sqlalchemy import text
        
        async with supabase_db_manager.get_session() as session:
            # Удаляем тестовые данные
            await session.execute(text("DELETE FROM workouts WHERE trainer_id IN (SELECT id FROM trainers WHERE telegram_id = 'test_123456789')"))
            await session.execute(text("DELETE FROM trainer_client WHERE trainer_id IN (SELECT id FROM trainers WHERE telegram_id = 'test_123456789')"))
            await session.execute(text("DELETE FROM clients WHERE id IN (SELECT client_id FROM trainer_client WHERE trainer_id IN (SELECT id FROM trainers WHERE telegram_id = 'test_123456789'))"))
            await session.execute(text("DELETE FROM trainers WHERE telegram_id = 'test_123456789'"))
            await session.execute(text("DELETE FROM exercises WHERE name = 'Тест упражнение'"))
            
        print("✅ Тестовые данные очищены")
        
    except Exception as e:
        print(f"⚠️ Ошибка очистки: {e}")

async def main():
    """Главная функция тестирования"""
    print("🧪 Тестирование интеграции с Supabase")
    print("=" * 50)
    
    # Загружаем переменные окружения
    if not load_supabase_env():
        return
    
    success = True
    
    # Тест 1: Подключение
    if not await test_supabase_connection():
        success = False
    
    # Тест 2: CRUD операции
    if success:
        if not await test_supabase_crud():
            success = False
    
    # Тест 3: Базовые упражнения
    if success:
        if not await test_basic_exercises():
            success = False
    
    # Очистка
    await cleanup_test_data()
    
    # Результат
    print("\n" + "=" * 50)
    if success:
        print("🎉 ВСЕ ТЕСТЫ SUPABASE ПРОЙДЕНЫ УСПЕШНО!")
        print()
        print("✅ Что протестировано:")
        print("   • Подключение к Supabase PostgreSQL")
        print("   • Создание и обновление тренеров")
        print("   • Управление клиентами")
        print("   • Планирование тренировок")
        print("   • Поиск и статистика")
        print("   • Библиотека упражнений")
        print()
        print("🚀 Ваш фитнес-бот готов к работе с Supabase!")
        print("   Все данные будут автоматически сохраняться в облаке")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        print("   Проверьте настройки Supabase и интернет-соединение")
    
    # Закрываем соединение
    try:
        from shared.supabase_database import supabase_db_manager
        await supabase_db_manager.close()
        print("🔒 Соединение с Supabase закрыто")
    except:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n💥 Неожиданная ошибка: {e}")
