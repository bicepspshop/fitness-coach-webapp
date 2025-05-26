# 🏋️‍♂️ Фитнес-тренер Telegram Bot

**Полнофункциональный бот-помощник для фитнес-тренеров** с веб-приложением для управления клиентами, планирования тренировок и ведения аналитики.

## ✨ Возможности

### 👥 Управление клиентами
- ➕ Добавление новых клиентов с полной анкетой
- 📋 Просмотр списка всех клиентов
- 🔍 Поиск клиентов по имени/фамилии
- ✏️ Редактирование информации о клиентах
- 🗑️ Удаление клиентов с подтверждением
- 📊 Детальная статистика по клиентской базе

### 💪 Планирование тренировок
- 📅 Создание расписания тренировок
- 🏃‍♂️ Конструктор программ упражнений
- ⏰ Напоминания клиентам о тренировках
- 📝 Отчеты после тренировок

### 📊 Аналитика и отчеты
- 📈 Графики прогресса клиентов
- 💰 Финансовая отчетность
- 🎯 Анализ достижения целей
- 📋 Экспорт данных

### 🌐 Веб-приложение
- 🖥️ Полнофункциональная веб-панель
- 📱 Адаптивный дизайн для мобильных устройств
- ⚡ Быстрая работа с данными
- 🔄 Синхронизация с Telegram ботом

### ☁️ Поддержка Supabase
- 🗄️ Облачная база данных PostgreSQL
- 🔄 Автоматическая синхронизация данных
- 📈 Масштабируемость и надежность
- 🔒 Защищенное хранение данных
- 🌐 Веб-панель управления БД

## 🚀 Быстрый старт

### Выберите версию:

#### ☁️ **Рекомендуется: Supabase (облачная БД)**
```bash
# 1. Настройте Supabase
cp .env.supabase.example .env.supabase
# Отредактируйте .env.supabase своими данными Supabase

# 2. Запустите бота с облачной БД
python run_bot_supabase.py
```

#### 💾 **Локальная версия (SQLite)**
```bash
# 1. Настройте локальную БД
cp .env.example .env
# Отредактируйте .env

# 2. Запустите обычного бота
python run_bot.py
```

### ☁️ Настройка Supabase (рекомендуется)

1. **Создайте проект в Supabase:**
   - Перейдите на [supabase.com](https://supabase.com)
   - Создайте новый проект
   - Скопируйте URL проекта и API ключи

2. **Настройте конфигурацию:**
   ```bash
   cp .env.supabase.example .env.supabase
   ```
   
   Заполните `.env.supabase`:
   ```env
   BOT_TOKEN=your_bot_token_here
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your_anon_key_here
   SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
   DATABASE_URL=postgresql://postgres:your_password@db.your-project.supabase.co:5432/postgres
   ```

3. **Запустите с Supabase:**
   ```bash
   python run_bot_supabase.py
   ```

4. **Протестируйте подключение:**
   ```bash
   python test_supabase.py
   ```

### 💾 Локальная установка (SQLite)

1. **Установите зависимости:**
   ```bash
   cd bot
   pip install -r requirements.txt
   ```

2. **Настройте локальную конфигурацию:**
   ```bash
   cp .env.example .env
   ```
   
   Отредактируйте `.env`:
   ```env
   BOT_TOKEN=your_bot_token_here
   WEB_APP_URL=https://bicepspshop.github.io/fitness-coach-webapp
   DATABASE_URL=sqlite:///coach.db
   DEBUG=True
   ```

3. **Запустите локального бота:**
   ```bash
   python run_bot.py
   ```

4. **Протестируйте:**
   ```bash
   python test_bot.py
   ```

## 📋 Команды бота

- `/start` - Главное меню и регистрация
- `/help` - Справка по использованию
- `/clients` - Управление клиентами
- `/workouts` - Планирование тренировок
- `/stats` - Статистика и аналитика
- `/profile` - Профиль тренера

## ☁️ Преимущества Supabase версии

### 🔄 **Синхронизация данных**
- Доступ к данным с любого устройства
- Автоматическое резервное копирование
- Real-time обновления

### 📈 **Масштабируемость**
- Поддержка тысяч клиентов
- Неограниченное количество тренировок
- Высокая производительность

### 🔒 **Безопасность**
- Шифрование данных
- Защищенные API
- Контроль доступа

### 🌐 **Веб-панель управления**
- Прямой доступ к базе данных
- SQL редактор
- Мониторинг производительности
- Логи и аналитика

### 🚀 **Готовые возможности**
- Автоматическая настройка таблиц
- Базовая библиотека упражнений
- Очистка от демо-данных
- Полная документация

## 🗂️ Структура проекта

```
coach/
├── bot/                           # Telegram бот
│   ├── handlers/                  # Обработчики команд
│   │   ├── clients.py            # Управление клиентами (SQLite)
│   │   ├── clients_supabase.py   # Управление клиентами (Supabase) ☁️
│   │   ├── workouts.py           # Тренировки (SQLite)
│   │   ├── workouts_supabase.py  # Тренировки (Supabase) ☁️
│   │   └── clients_stats.py      # Статистика клиентов
│   ├── keyboards/                # Клавиатуры
│   ├── utils/                   # Вспомогательные модули
│   ├── main.py                  # Главный файл бота (SQLite)
│   ├── main_supabase.py         # Главный файл бота (Supabase) ☁️
│   └── requirements.txt         # Зависимости
├── shared/                      # Общие модули
│   ├── models.py               # Модели базы данных
│   ├── database.py             # Работа с SQLite БД
│   ├── supabase_database.py    # Работа с Supabase БД ☁️
│   ├── config.py               # Конфигурация (SQLite)
│   └── config_supabase.py      # Конфигурация (Supabase) ☁️
├── web/                        # Веб-приложение
├── run_bot.py                  # Запуск SQLite версии
├── run_bot_supabase.py         # Запуск Supabase версии ☁️
├── test_supabase.py            # Тестирование Supabase ☁️
├── clear_demo_data.py          # Очистка демо-данных ☁️
└── docker-compose.yml          # Docker контейнеры
```

## 🔧 Конфигурация

### ☁️ Supabase (рекомендуется)
Для облачной базы данных PostgreSQL:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
DATABASE_URL=postgresql://postgres:password@db.your-project.supabase.co:5432/postgres
```

### 💾 SQLite (локальная)
Для локальной базы данных:

```env
DATABASE_URL=sqlite:///coach.db
```

### 🌐 Веб-приложение
Веб-приложение развернуто на GitHub Pages:

```env
WEB_APP_URL=https://bicepspshop.github.io/fitness-coach-webapp
```

Для собственного домена:
```env
WEB_APP_URL=https://yourdomain.com/webapp
```

## 🐳 Docker

### Локальная версия:
```bash
docker-compose up -d
```

### Supabase версия:
```bash
# Скоро будет добавлена конфигурация для Supabase
```

## 📱 Использование

### Добавление клиента

1. Отправьте `/clients` боту
2. Нажмите "➕ Добавить клиента"
3. Заполните анкету пошагово
4. Подтвердите сохранение
5. ☁️ **Supabase**: Данные автоматически сохраняются в облаке

### Планирование тренировки

1. Отправьте `/workouts` боту
2. Нажмите "➕ Создать тренировку"
3. Выберите клиента
4. Укажите дату и время ("сегодня 18:00", "завтра 15:30")
5. Выберите тип тренировки
6. ☁️ **Supabase**: Тренировка синхронизируется с веб-приложением

### Поиск клиентов

1. В меню клиентов нажмите "🔍 Поиск"
2. Введите часть имени или фамилии
3. Выберите нужного клиента из результатов
4. ☁️ **Supabase**: Поиск работает по облачной базе данных

### Просмотр статистики

1. Нажмите "📊 Статистика" в меню клиентов
2. Изучите распределение по целям, полу, активности
3. Посмотрите средние показатели
4. ☁️ **Supabase**: Статистика в реальном времени

## 🛠️ Разработка

### Добавление новых возможностей

1. Создайте новый handler в `bot/handlers/`
2. Для Supabase версии создайте `*_supabase.py`
3. Добавьте роутер в `main.py` или `main_supabase.py`
4. Обновите клавиатуры в `keyboards/`
5. При необходимости расширьте модели в `shared/models.py`

### Тестирование

#### SQLite версия:
```bash
python test_bot.py        # Тест базы данных
flake8 bot/              # Проверка синтаксиса
DEBUG=True python bot/main.py  # Запуск с отладкой
```

#### Supabase версия:
```bash
python test_supabase.py          # Тест Supabase подключения
python clear_demo_data.py        # Очистка демо-данных
DEBUG=True python bot/main_supabase.py  # Запуск с отладкой
```

### Миграция с SQLite на Supabase

1. Экспортируйте данные из SQLite:
   ```bash
   python export_clients_to_web.py
   ```

2. Настройте Supabase конфигурацию

3. Запустите Supabase версию:
   ```bash
   python run_bot_supabase.py
   ```

4. Импортируйте данные через бота

## 📋 TODO

### ✅ Завершено
- [x] Управление клиентами
- [x] Планирование тренировок  
- [x] Статистика и аналитика
- [x] Веб-приложение
- [x] Интеграция с Supabase
- [x] Облачная синхронизация
- [x] Очистка демо-данных
- [x] Полная документация

### 🔄 В разработке
- [ ] Планы питания
- [ ] Интеграция с фитнес-трекерами
- [ ] Push-уведомления
- [ ] Групповые тренировки
- [ ] Финансовая отчетность
- [ ] Экспорт данных в Excel/PDF
- [ ] Мобильное приложение
- [ ] API для сторонних интеграций

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Внесите изменения
4. Протестируйте изменения:
   - SQLite: `python test_bot.py`
   - Supabase: `python test_supabase.py`
5. Создайте Pull Request

### Стиль кода
- Используйте Python 3.11+
- Следуйте PEP 8
- Добавляйте типизацию где возможно
- Пишите docstrings для функций
- Создавайте отдельные версии для Supabase

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 📞 Поддержка

По вопросам обращайтесь:
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/fitness-coach-bot/issues)
- 💬 **Telegram**: @your_username
- 📧 **Email**: support@example.com
- 📖 **Документация**: См. файлы `*.md` в репозитории

### Полезные ссылки
- 📋 [Настройка Supabase](SUPABASE_INTEGRATION_COMPLETE.md)
- 🧹 [Очистка демо-данных](DEMO_DATA_CLEANED.md)
- 🚀 [Быстрый старт](QUICK_START_NEW.md)
- 🔧 [Руководство разработчика](DEVELOPMENT_REPORT.md)

---

**Создано с ❤️ для фитнес-тренеров**

[![Supabase](https://img.shields.io/badge/Database-Supabase-green)](https://supabase.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![aiogram](https://img.shields.io/badge/Framework-aiogram_3.x-blue)](https://aiogram.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
