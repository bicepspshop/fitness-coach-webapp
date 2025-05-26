import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from contextlib import asynccontextmanager
from shared.models import Base
from shared.config_supabase import supabase_config, SUPABASE_DATABASE_CONFIG
import logging

logger = logging.getLogger(__name__)

class SupabaseDatabaseManager:
    def __init__(self):
        self.engine = None
        self.async_session_maker = None
        self.is_initialized = False
    
    async def initialize(self):
        """Инициализация базы данных Supabase"""
        if self.is_initialized:
            return
            
        try:
            # Создаем подключение к Supabase PostgreSQL
            database_url = supabase_config.DATABASE_URL.replace(
                'postgresql://', 'postgresql+asyncpg://'
            )
            
            self.engine = create_async_engine(
                database_url,
                **SUPABASE_DATABASE_CONFIG['postgresql']
            )
            
            self.async_session_maker = async_sessionmaker(
                self.engine, 
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Создаем таблицы в Supabase
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            logger.info("✅ Supabase база данных успешно инициализирована")
            logger.info(f"🔗 Подключение к: {supabase_config.SUPABASE_PROJECT_ID}.supabase.co")
            self.is_initialized = True
            
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации Supabase: {e}")
            raise
    
    @asynccontextmanager
    async def get_session(self):
        """Контекстный менеджер для работы с сессией Supabase"""
        if not self.is_initialized:
            await self.initialize()
            
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"❌ Ошибка в сессии Supabase: {e}")
                raise
            finally:
                await session.close()
    
    async def health_check(self):
        """Проверка состояния Supabase"""
        try:
            async with self.get_session() as session:
                result = await session.execute(text("SELECT 1 as health_check"))
                return result.scalar() == 1
        except Exception as e:
            logger.error(f"❌ Проверка здоровья Supabase не пройдена: {e}")
            return False
    
    async def close(self):
        """Закрытие соединения с Supabase"""
        if self.engine:
            await self.engine.dispose()
            logger.info("🔒 Соединение с Supabase закрыто")

# Глобальный экземпляр менеджера Supabase
supabase_db_manager = SupabaseDatabaseManager()

# Вспомогательные функции для работы с моделями в Supabase
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from shared.models import Trainer, Client, Workout, Exercise, WorkoutStatus, trainer_client_table

class SupabaseTrainerService:
    @staticmethod
    async def create_trainer(telegram_id: str, **kwargs):
        """Создание нового тренера в Supabase"""
        async with supabase_db_manager.get_session() as session:
            trainer = Trainer(telegram_id=telegram_id, **kwargs)
            session.add(trainer)
            await session.flush()
            logger.info(f"👤 Тренер создан в Supabase: {trainer.first_name} (ID: {trainer.id})")
            return trainer
    
    @staticmethod
    async def get_trainer_by_telegram_id(telegram_id: str):
        """Получение тренера из Supabase по Telegram ID"""
        async with supabase_db_manager.get_session() as session:
            result = await session.execute(
                select(Trainer).where(Trainer.telegram_id == telegram_id)
            )
            trainer = result.scalar_one_or_none()
            if trainer:
                logger.info(f"👤 Тренер найден в Supabase: {trainer.first_name}")
            return trainer
    
    @staticmethod
    async def update_trainer(trainer_id: int, **kwargs):
        """Обновление данных тренера в Supabase"""
        async with supabase_db_manager.get_session() as session:
            await session.execute(
                update(Trainer).where(Trainer.id == trainer_id).values(**kwargs)
            )
            logger.info(f"👤 Тренер обновлен в Supabase: ID {trainer_id}")

class SupabaseClientService:
    @staticmethod
    async def create_client(trainer_id: int, **kwargs):
        """Создание нового клиента в Supabase"""
        async with supabase_db_manager.get_session() as session:
            client = Client(**kwargs)
            session.add(client)
            await session.flush()
            
            # Связываем клиента с тренером
            trainer = await session.get(Trainer, trainer_id)
            if trainer:
                trainer.clients.append(client)
            
            await session.refresh(client)
            logger.info(f"👥 Клиент создан в Supabase: {client.first_name} (ID: {client.id})")
            return client
    
    @staticmethod
    async def get_trainer_clients(trainer_id: int, limit: int = None, offset: int = 0):
        """Получение всех клиентов тренера из Supabase"""
        async with supabase_db_manager.get_session() as session:
            query = (
                select(Client)
                .join(trainer_client_table)
                .where(trainer_client_table.c.trainer_id == trainer_id)
                .order_by(Client.created_at.desc())
            )
            
            if limit:
                query = query.limit(limit).offset(offset)
                
            result = await session.execute(query)
            clients = result.scalars().all()
            logger.info(f"👥 Загружено клиентов из Supabase: {len(clients)}")
            return clients
    
    @staticmethod
    async def get_client_by_id(client_id: int):
        """Получение клиента из Supabase по ID"""
        async with supabase_db_manager.get_session() as session:
            result = await session.execute(
                select(Client).where(Client.id == client_id)
            )
            return result.scalar_one_or_none()
    
    @staticmethod
    async def update_client(client_id: int, **kwargs):
        """Обновление данных клиента в Supabase"""
        async with supabase_db_manager.get_session() as session:
            await session.execute(
                update(Client).where(Client.id == client_id).values(**kwargs)
            )
            
            # Возвращаем обновленного клиента
            result = await session.execute(
                select(Client).where(Client.id == client_id)
            )
            logger.info(f"👥 Клиент обновлен в Supabase: ID {client_id}")
            return result.scalar_one_or_none()
    
    @staticmethod
    async def delete_client(client_id: int):
        """Удаление клиента из Supabase"""
        async with supabase_db_manager.get_session() as session:
            await session.execute(
                delete(Client).where(Client.id == client_id)
            )
            logger.info(f"👥 Клиент удален из Supabase: ID {client_id}")
            return True
    
    @staticmethod
    async def search_clients(trainer_id: int, query: str):
        """Поиск клиентов в Supabase по имени/фамилии"""
        async with supabase_db_manager.get_session() as session:
            search_pattern = f"%{query}%"
            result = await session.execute(
                select(Client)
                .join(trainer_client_table)
                .where(
                    trainer_client_table.c.trainer_id == trainer_id,
                    (Client.first_name.ilike(search_pattern) | 
                     Client.last_name.ilike(search_pattern))
                )
                .order_by(Client.first_name)
            )
            clients = result.scalars().all()
            logger.info(f"🔍 Найдено клиентов в Supabase: {len(clients)} по запросу '{query}'")
            return clients
    
    @staticmethod
    async def get_clients_count(trainer_id: int):
        """Получение количества клиентов тренера из Supabase"""
        async with supabase_db_manager.get_session() as session:
            result = await session.execute(
                select(func.count(Client.id))
                .join(trainer_client_table)
                .where(trainer_client_table.c.trainer_id == trainer_id)
            )
            count = result.scalar() or 0
            logger.info(f"📊 Количество клиентов в Supabase: {count}")
            return count

class SupabaseWorkoutService:
    @staticmethod
    async def create_workout(trainer_id: int, client_id: int, **kwargs):
        """Создание новой тренировки в Supabase"""
        async with supabase_db_manager.get_session() as session:
            workout_data = {
                'trainer_id': trainer_id,
                'client_id': client_id,
                **kwargs
            }
            
            # Обрабатываем workout_type
            if 'workout_type' in kwargs:
                workout_data['trainer_notes'] = f"[{kwargs['workout_type']}] " + (workout_data.get('trainer_notes', '') or '')
                del workout_data['workout_type']
            
            workout = Workout(**workout_data)
            session.add(workout)
            await session.flush()
            await session.refresh(workout)
            logger.info(f"💪 Тренировка создана в Supabase: ID {workout.id}")
            return workout
    
    @staticmethod
    async def get_workout_by_id(workout_id: int):
        """Получение тренировки из Supabase по ID"""
        async with supabase_db_manager.get_session() as session:
            result = await session.execute(
                select(Workout)
                .options(selectinload(Workout.client))
                .where(Workout.id == workout_id)
            )
            return result.scalar_one_or_none()
    
    @staticmethod
    async def get_upcoming_workouts(trainer_id: int, limit: int = 10):
        """Получение ближайших тренировок из Supabase"""
        async with supabase_db_manager.get_session() as session:
            from datetime import datetime
            result = await session.execute(
                select(Workout)
                .options(selectinload(Workout.client))
                .where(
                    Workout.trainer_id == trainer_id,
                    Workout.scheduled_date >= datetime.now(),
                    Workout.status == WorkoutStatus.PLANNED
                )
                .order_by(Workout.scheduled_date)
                .limit(limit)
            )
            workouts = result.scalars().all()
            logger.info(f"📅 Загружено ближайших тренировок из Supabase: {len(workouts)}")
            return workouts
    
    @staticmethod
    async def get_today_workouts(trainer_id: int):
        """Получение тренировок на сегодня из Supabase"""
        async with supabase_db_manager.get_session() as session:
            from datetime import datetime, date
            today = date.today()
            result = await session.execute(
                select(Workout)
                .options(selectinload(Workout.client))
                .where(
                    Workout.trainer_id == trainer_id,
                    func.date(Workout.scheduled_date) == today
                )
                .order_by(Workout.scheduled_date)
            )
            workouts = result.scalars().all()
            logger.info(f"📅 Тренировок на сегодня в Supabase: {len(workouts)}")
            return workouts
    
    @staticmethod
    async def get_client_workouts(client_id: int, limit: int = None):
        """Получение всех тренировок клиента из Supabase"""
        async with supabase_db_manager.get_session() as session:
            query = (
                select(Workout)
                .options(selectinload(Workout.trainer))
                .where(Workout.client_id == client_id)
                .order_by(Workout.scheduled_date.desc())
            )
            
            if limit:
                query = query.limit(limit)
            
            result = await session.execute(query)
            workouts = result.scalars().all()
            logger.info(f"💪 Тренировок клиента {client_id} в Supabase: {len(workouts)}")
            return workouts
    
    @staticmethod
    async def get_workouts_count(trainer_id: int):
        """Получение количества тренировок тренера из Supabase"""
        async with supabase_db_manager.get_session() as session:
            result = await session.execute(
                select(func.count(Workout.id))
                .where(Workout.trainer_id == trainer_id)
            )
            count = result.scalar() or 0
            logger.info(f"📊 Количество тренировок в Supabase: {count}")
            return count
    
    @staticmethod
    async def update_workout_plan(workout_id: int, exercises_plan: list):
        """Обновление плана упражнений в Supabase"""
        async with supabase_db_manager.get_session() as session:
            await session.execute(
                update(Workout)
                .where(Workout.id == workout_id)
                .values(exercises=exercises_plan)
            )
            logger.info(f"💪 План тренировки обновлен в Supabase: ID {workout_id}")
    
    @staticmethod
    async def update_workout_status(workout_id: int, status: str, **kwargs):
        """Обновление статуса тренировки в Supabase"""
        async with supabase_db_manager.get_session() as session:
            update_data = {'status': status, **kwargs}
            
            if status == 'completed' and 'completed_at' not in update_data:
                from datetime import datetime
                update_data['completed_at'] = datetime.now()
            
            await session.execute(
                update(Workout)
                .where(Workout.id == workout_id)
                .values(**update_data)
            )
            logger.info(f"💪 Статус тренировки обновлен в Supabase: ID {workout_id} -> {status}")
    
    @staticmethod
    async def delete_workout(workout_id: int):
        """Удаление тренировки из Supabase"""
        async with supabase_db_manager.get_session() as session:
            await session.execute(
                delete(Workout).where(Workout.id == workout_id)
            )
            logger.info(f"💪 Тренировка удалена из Supabase: ID {workout_id}")
            return True

class SupabaseExerciseService:
    @staticmethod
    async def get_exercises_by_category(category: str):
        """Получение упражнений по категории из Supabase"""
        async with supabase_db_manager.get_session() as session:
            result = await session.execute(
                select(Exercise).where(Exercise.category == category)
            )
            return result.scalars().all()
    
    @staticmethod
    async def get_exercise_by_id(exercise_id: int):
        """Получение упражнения из Supabase по ID"""
        async with supabase_db_manager.get_session() as session:
            result = await session.execute(
                select(Exercise).where(Exercise.id == exercise_id)
            )
            return result.scalar_one_or_none()
    
    @staticmethod
    async def create_exercise(name: str, category: str, **kwargs):
        """Создание нового упражнения в Supabase"""
        async with supabase_db_manager.get_session() as session:
            exercise = Exercise(name=name, category=category, **kwargs)
            session.add(exercise)
            await session.flush()
            await session.refresh(exercise)
            logger.info(f"🏋️ Упражнение создано в Supabase: {exercise.name}")
            return exercise
    
    @staticmethod
    async def search_exercises(query: str):
        """Поиск упражнений в Supabase по названию"""
        async with supabase_db_manager.get_session() as session:
            search_pattern = f"%{query}%"
            result = await session.execute(
                select(Exercise).where(Exercise.name.ilike(search_pattern))
            )
            return result.scalars().all()

# Функция для инициализации базовых упражнений в Supabase
async def init_basic_exercises():
    """Инициализация базовых упражнений в Supabase (без демо-клиентов)"""
    async with supabase_db_manager.get_session() as session:
        # Проверяем, есть ли уже упражнения
        result = await session.execute(select(Exercise).limit(1))
        if result.scalar_one_or_none():
            logger.info("🏋️ Базовые упражнения уже есть в Supabase")
            return  # Упражнения уже есть
        
        logger.info("🏋️ Создание базовых упражнений в Supabase...")
        
        # Создаем только базовые упражнения (без демо-клиентов/тренировок)
        exercises = [
            # Основные упражнения для библиотеки
            Exercise(
                name="Отжимания",
                category="chest",
                muscle_groups=["chest", "triceps", "shoulders"],
                equipment="bodyweight",
                difficulty="beginner",
                description="Классические отжимания от пола",
                instructions="Примите упор лежа, опуститесь до касания грудью пола, вернитесь в исходное положение",
                calories_per_minute=8.0
            ),
            Exercise(
                name="Приседания",
                category="legs",
                muscle_groups=["quadriceps", "glutes", "hamstrings"],
                equipment="bodyweight",
                difficulty="beginner",
                description="Базовые приседания с собственным весом",
                instructions="Поставьте ноги на ширине плеч, опуститесь, сгибая колени до 90 градусов",
                calories_per_minute=6.0
            ),
            Exercise(
                name="Планка",
                category="core",
                muscle_groups=["core", "shoulders"],
                equipment="bodyweight",
                difficulty="beginner",
                description="Статическое упражнение для укрепления кора",
                instructions="Примите упор лежа на предплечьях, держите тело прямой линией",
                calories_per_minute=5.0
            ),
        ]
        
        for exercise in exercises:
            session.add(exercise)
        
        logger.info(f"✅ Добавлено {len(exercises)} базовых упражнений в Supabase")

# Инициализация при импорте модуля
async def init_supabase_database():
    """Функция для инициализации Supabase при запуске приложения"""
    await supabase_db_manager.initialize()
    await init_basic_exercises()
    logger.info("✅ Supabase база данных полностью инициализирована (без демо-данных)")
    logger.info("🚀 Готово к добавлению ваших клиентов и тренировок!")
