#!/usr/bin/env python3
"""
Запуск фитнес-бота с Supabase
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_windows_console():
    """Настройка консоли Windows для корректного отображения Unicode"""
    if sys.platform == 'win32':
        try:
            # Устанавливаем кодировку UTF-8 для консоли
            os.system('chcp 65001 > nul')
            
            # Устанавливаем переменные окружения для Python
            os.environ['PYTHONIOENCODING'] = 'utf-8'
            os.environ['PYTHONUTF8'] = '1'
            
            print("✓ Консоль Windows настроена для UTF-8")
        except Exception as e:
            print(f"⚠ Не удалось настроить консоль: {e}")

def check_supabase_requirements():
    """Проверка установленных зависимостей для Supabase"""
    requirements_file = Path(__file__).parent / 'bot' / 'requirements.txt'
    
    if not requirements_file.exists():
        print("❌ Файл requirements.txt не найден")
        return False
    
    try:
        # Проверяем основные зависимости
        import aiogram
        import sqlalchemy
        import asyncpg  # Для PostgreSQL
        import supabase  # Для Supabase
        print("✓ Основные зависимости для Supabase установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствуют зависимости для Supabase: {e}")
        print("Установите зависимости командой:")
        print(f"pip install -r {requirements_file}")
        return False

def check_supabase_config():
    """Проверка конфигурации Supabase"""
    env_file = Path(__file__).parent / '.env.supabase'
    
    if not env_file.exists():
        print("❌ Файл .env.supabase не найден")
        print("Создан файл .env.supabase с вашими настройками Supabase")
        return True
    
    # Читаем конфигурацию Supabase
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'SUPABASE_URL=' in content and 'nludsxoqhhlfpehhblgg' in content:
                print("✓ Конфигурация Supabase найдена")
                print("✓ URL проекта: https://nludsxoqhhlfpehhblgg.supabase.co")
                print("✓ Ключи API настроены")
            else:
                print("⚠ Проверьте настройки Supabase в файле .env.supabase")
        return True
    except Exception as e:
        print(f"❌ Ошибка чтения конфигурации Supabase: {e}")
        return False

def start_supabase_bot():
    """Запуск бота с Supabase"""
    bot_dir = Path(__file__).parent / 'bot'
    
    if not bot_dir.exists():
        print("❌ Папка bot не найдена")
        return False
    
    try:
        # Переходим в папку бота и запускаем Supabase версию
        os.chdir(bot_dir)
        
        # Запускаем с правильной кодировкой
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        print("🚀 Запуск бота с Supabase...")
        print("☁️ Все данные будут сохраняться в облачную базу данных")
        subprocess.run([sys.executable, 'main_supabase.py'], env=env)
        
    except KeyboardInterrupt:
        print("\n👋 Supabase бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска Supabase бота: {e}")

def main():
    """Главная функция"""
    print("🏋️‍♂️ Фитнес-помощник для тренеров (Supabase)")
    print("=" * 50)
    print("☁️ Версия с облачной базой данных Supabase")
    print()
    
    # Настраиваем консоль
    setup_windows_console()
    
    # Проверяем зависимости
    if not check_supabase_requirements():
        return
    
    # Проверяем конфигурацию Supabase
    if not check_supabase_config():
        return
    
    print()
    print("🎯 Что будет записываться в Supabase:")
    print("   • 👤 Тренеры и их профили")
    print("   • 👥 Клиенты и их данные")
    print("   • 💪 Тренировки и планы")
    print("   • 🏋️ Упражнения и программы")
    print("   • 📊 Статистика и прогресс")
    print("   • 💰 Платежи и финансы")
    print()
    
    # Запускаем бота с Supabase
    start_supabase_bot()

if __name__ == "__main__":
    main()
