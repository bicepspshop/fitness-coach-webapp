#!/usr/bin/env python3
"""
Скрипт для очистки демо-данных из Supabase
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
        return True
    else:
        print(f"❌ Файл .env.supabase не найден")
        return False

async def clear_all_demo_data():
    """Очистка всех демо-данных из Supabase"""
    print("🧹 Очистка всех демо-данных из Supabase...")
    
    try:
        from shared.supabase_database import supabase_db_manager
        from sqlalchemy import text
        
        await supabase_db_manager.initialize()
        
        async with supabase_db_manager.get_session() as session:
            # Удаляем все данные (кроме базовых упражнений)
            
            # 1. Удаляем все тренировки
            result = await session.execute(text("DELETE FROM workouts"))
            print(f"🗑️ Удалено тренировок: {result.rowcount}")
            
            # 2. Удаляем связи тренер-клиент
            result = await session.execute(text("DELETE FROM trainer_client"))
            print(f"🗑️ Удалено связей тренер-клиент: {result.rowcount}")
            
            # 3. Удаляем всех клиентов
            result = await session.execute(text("DELETE FROM clients"))
            print(f"🗑️ Удалено клиентов: {result.rowcount}")
            
            # 4. Удаляем всех тренеров
            result = await session.execute(text("DELETE FROM trainers"))
            print(f"🗑️ Удалено тренеров: {result.rowcount}")
            
            # 5. Удаляем замеры
            result = await session.execute(text("DELETE FROM measurements"))
            print(f"🗑️ Удалено замеров: {result.rowcount}")
            
            # 6. Удаляем планы питания
            result = await session.execute(text("DELETE FROM nutrition_plans"))
            print(f"🗑️ Удалено планов питания: {result.rowcount}")
            
            # 7. Удаляем платежи
            result = await session.execute(text("DELETE FROM payments"))
            print(f"🗑️ Удалено платежей: {result.rowcount}")
            
            # 8. Удаляем уведомления
            result = await session.execute(text("DELETE FROM notifications"))
            print(f"🗑️ Удалено уведомлений: {result.rowcount}")
            
            # 9. Оставляем только базовые упражнения
            result = await session.execute(text("""
                DELETE FROM exercises 
                WHERE name NOT IN ('Отжимания', 'Приседания', 'Планка')
            """))
            print(f"🗑️ Удалено лишних упражнений: {result.rowcount}")
            
            # Проверяем, что осталось
            result = await session.execute(text("SELECT COUNT(*) FROM exercises"))
            exercises_count = result.scalar()
            print(f"✅ Осталось базовых упражнений: {exercises_count}")
            
        print("✅ Все демо-данные успешно удалены из Supabase!")
        print("🚀 База данных готова для ваших реальных данных!")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка очистки данных: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Главная функция"""
    print("🧹 Очистка демо-данных из Supabase")
    print("=" * 40)
    
    # Загружаем переменные окружения
    if not load_supabase_env():
        return
    
    # Подтверждение
    print("\n⚠️  ВНИМАНИЕ! Это действие удалит ВСЕ данные из Supabase:")
    print("   • Всех тренеров")
    print("   • Всех клиентов") 
    print("   • Все тренировки")
    print("   • Все замеры")
    print("   • Все планы питания")
    print("   • Все платежи")
    print("   • Все уведомления")
    print("\n✅ Останутся только базовые упражнения")
    print("\n🚫 Это действие НЕОБРАТИМО!")
    
    confirm = input("\nВы уверены? Введите 'ДА' для подтверждения: ")
    
    if confirm.upper() != 'ДА':
        print("❌ Операция отменена")
        return
    
    # Очистка данных
    success = await clear_all_demo_data()
    
    if success:
        print("\n" + "=" * 40)
        print("🎉 ОЧИСТКА ЗАВЕРШЕНА УСПЕШНО!")
        print()
        print("✅ Что сделано:")
        print("   • Удалены все демо-данные из Supabase")
        print("   • Оставлены только базовые упражнения") 
        print("   • База готова для ваших реальных данных")
        print()
        print("🚀 Следующие шаги:")
        print("   1. Запустите бота: python run_bot_supabase.py")
        print("   2. Добавьте своих клиентов через /clients")
        print("   3. Создайте тренировки через /workouts")
        print("   4. Проверьте синхронизацию в веб-приложении")
    else:
        print("\n❌ ОЧИСТКА НЕ ЗАВЕРШЕНА")
        print("   Проверьте подключение к Supabase и попробуйте еще раз")
    
    # Закрываем соединение
    try:
        from shared.supabase_database import supabase_db_manager
        await supabase_db_manager.close()
    except:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Операция прервана пользователем")
    except Exception as e:
        print(f"\n💥 Неожиданная ошибка: {e}")
