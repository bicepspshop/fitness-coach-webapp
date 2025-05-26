import os
from typing import Optional, List

class SupabaseConfig:
    """Конфигурация для работы с Supabase"""
    
    def __init__(self):
        # Telegram Bot
        self.BOT_TOKEN: str = os.getenv("BOT_TOKEN", "7503397913:AAFp_BqK1kzVvQT_nmDFDRJ2avyd-kX3AIQ")
        self.WEBHOOK_URL: Optional[str] = os.getenv("WEBHOOK_URL")
        
        # Supabase Configuration
        self.SUPABASE_URL: str = os.getenv("SUPABASE_URL", "https://nludsxoqhhlfpehhblgg.supabase.co")
        self.SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5sdWRzeG9xaGhsZnBlaGhibGdnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgyODUyNjEsImV4cCI6MjA2Mzg2MTI2MX0.o6DtsgGgpuNQFIL9Gh2Ba-xScVW20dU_IDg4QAYYXxQ")
        self.SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5sdWRzeG9xaGhsZnBlaGhibGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODI4NTI2MSwiZXhwIjoyMDYzODYxMjYxfQ.N7jFYv-mjQeitzSLlKhooeeck-4wYnmQcO3YiVNfACI")
        
        # Database URL (PostgreSQL через Supabase)
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:APSebobILxqjP5ol@db.nludsxoqhhlfpehhblgg.supabase.co:5432/postgres")
        
        # Web App
        self.WEB_APP_URL: str = os.getenv("WEB_APP_URL", "https://bicepspshop.github.io/fitness-coach-webapp")
        
        # Admin
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        self.ADMIN_IDS: List[int] = [int(x) for x in admin_ids_str.split(",") if x.strip()]
        
        # Features
        self.DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
        
        # Limits
        self.MAX_CLIENTS_PER_TRAINER: int = int(os.getenv("MAX_CLIENTS_PER_TRAINER", "1000"))
        self.MAX_WORKOUTS_PER_CLIENT: int = int(os.getenv("MAX_WORKOUTS_PER_CLIENT", "10000"))
        
        # Supabase Project Info
        self.SUPABASE_PROJECT_ID: str = os.getenv("SUPABASE_PROJECT_ID", "nludsxoqhhlfpehhblgg")
        self.SUPABASE_DB_PASSWORD: str = os.getenv("SUPABASE_DB_PASSWORD", "APSebobILxqjP5ol")

# Создаем глобальный экземпляр конфигурации для Supabase
supabase_config = SupabaseConfig()

# Выводим информацию о конфигурации
print(f"🔗 Supabase URL: {supabase_config.SUPABASE_URL}")
print(f"🔑 Anon Key настроен: {supabase_config.SUPABASE_ANON_KEY[:20]}...")
print(f"🔑 Service Role настроен: {supabase_config.SUPABASE_SERVICE_ROLE_KEY[:20]}...")
print(f"🗄️ Database URL: postgresql://postgres:***@db.{supabase_config.SUPABASE_PROJECT_ID}.supabase.co:5432/postgres")
print(f"🌐 Web App: {supabase_config.WEB_APP_URL}")
print(f"🔧 Debug mode: {supabase_config.DEBUG}")

# Настройки базы данных для Supabase PostgreSQL
SUPABASE_DATABASE_CONFIG = {
    'postgresql': {
        'echo': supabase_config.DEBUG,
        'pool_size': 20,
        'max_overflow': 30,
        'pool_pre_ping': True,
        'pool_recycle': 3600,  # 1 час
        'connect_args': {
            'server_settings': {
                'application_name': 'fitness_coach_bot',
            }
        }
    }
}
