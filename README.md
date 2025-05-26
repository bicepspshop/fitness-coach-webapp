# 🏋️‍♂️ Фитнес-помощник для тренеров

**Полнофункциональное веб-приложение для персональных фитнес-тренеров** с интеграцией Telegram WebApp для управления клиентами, планирования тренировок и ведения аналитики.

## ✨ Основные возможности

### 👥 Управление клиентами
- ➕ Добавление новых клиентов с подробной анкетой
- 📋 Просмотр списка всех клиентов с фильтрацией
- 🔍 Быстрый поиск клиентов по имени/фамилии
- ✏️ Редактирование информации о клиентах
- 📊 Детальная статистика по клиентской базе
- 🎯 Отслеживание целей и прогресса

### 💪 Планирование тренировок
- 📅 Календарный планировщик тренировок
- 🏃‍♂️ Создание программ упражнений
- ⏰ Управление расписанием
- 📝 Заметки и отчеты по тренировкам
- 📱 Уведомления клиентам

### 📊 Аналитика и отчеты
- 📈 Интерактивные графики прогресса
- 💰 Финансовая отчетность
- 🎯 Анализ достижения целей
- 📋 Статистика посещаемости
- 📊 Визуализация данных с Chart.js

### 📱 Telegram WebApp интеграция
- 🤖 Полная интеграция с Telegram Bot API
- 📱 Адаптивный дизайн для мобильных устройств
- ⚡ Быстрая работа и отзывчивый интерфейс
- 🎨 Автоматическая адаптация к теме Telegram
- 🔔 Push-уведомления через Telegram

## 🚀 Демо

**Живая демка**: [https://bicepspshop.github.io/fitness-coach-webapp](https://bicepspshop.github.io/fitness-coach-webapp)

### Как протестировать в Telegram:
1. Найдите бота `@YourFitnessCoachBot` в Telegram
2. Отправьте команду `/start`
3. Нажмите кнопку "Открыть веб-приложение"

## 🛠️ Технологии

### Frontend
- **HTML5/CSS3** - современная адаптивная верстка
- **Vanilla JavaScript** - без фреймворков, быстрая загрузка
- **Chart.js** - интерактивные графики и аналитика
- **Font Awesome** - иконки
- **CSS Grid/Flexbox** - гибкая сетка

### Интеграции
- **Telegram WebApp API** - полная интеграция с Telegram
- **Telegram Bot API** - обмен данными с ботом
- **Web Storage API** - локальное хранение данных

### Архитектура
- **Модульная структура** - разделение по компонентам
- **Event-driven** - слабая связанность компонентов
- **Progressive Web App** - возможности PWA
- **Mobile First** - приоритет мобильной версии

## 📂 Структура проекта

```
fitness-coach-webapp/
├── index.html              # Главная страница приложения
├── css/
│   ├── style.css           # Основные стили
│   └── components.css      # Стили компонентов
├── js/
│   ├── app.js             # Главное приложение
│   ├── clients.js         # Модуль клиентов
│   ├── workouts.js        # Модуль тренировок
│   ├── charts.js          # Модуль графиков
│   └── telegram.js        # Интеграция с Telegram
├── assets/
│   ├── avatar-placeholder.jpg
│   └── avatar-placeholder.svg
└── README.md
```

## 🎯 Основные страницы

### 🏠 Главная страница (Dashboard)
- Обзор статистики (клиенты, тренировки, доходы)
- Быстрые действия (добавить клиента, запланировать тренировку)
- Расписание на сегодня
- График прогресса клиентов

### 👥 Управление клиентами
- Список всех клиентов с карточками
- Поиск и фильтрация (все/активные/неактивные)
- Добавление новых клиентов через модальную форму
- Просмотр детальной информации

### 💪 Планирование тренировок
- Календарный вид (месяц/неделя/день)
- Добавление тренировок с привязкой к клиентам
- Управление статусами тренировок
- Заметки тренера

### 📊 Аналитика
- График новых клиентов по месяцам
- Диаграмма доходов
- Распределение типов тренировок
- Статистика посещаемости

### ⚙️ Настройки
- Профиль тренера
- Уведомления
- Настройки темы
- Языковые настройки

## 💡 Основные компоненты

### ClientsManager
```javascript
// Управление клиентами
const clientsManager = new ClientsManager();
clientsManager.setClients(clients);
clientsManager.filterAndRenderClients();
```

### WorkoutsManager
```javascript
// Управление тренировками
const workoutsManager = new WorkoutsManager();
workoutsManager.setWorkouts(workouts);
workoutsManager.renderCalendar();
```

### ChartsManager
```javascript
// Управление графиками
const chartsManager = new ChartsManager();
chartsManager.createProgressChart('canvas-id', data);
```

### TelegramIntegration
```javascript
// Интеграция с Telegram
const telegram = new TelegramIntegration();
telegram.showAlert('Сообщение');
telegram.hapticFeedback('impact');
```

## 🔧 Настройка и развертывание

### Локальная разработка
```bash
# Просто откройте index.html в браузере
# Или используйте локальный сервер:
python -m http.server 8000
# или
npx serve .
```

### GitHub Pages
1. Форкните репозиторий
2. В настройках репозитория включите GitHub Pages
3. Выберите ветку `main` как источник
4. Приложение будет доступно по адресу `https://username.github.io/fitness-coach-webapp`

### Интеграция с Telegram ботом
1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен бота
3. Настройте WebApp URL в боте:
```python
# В коде бота
web_app_url = "https://your-domain.com/fitness-coach-webapp"
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("🌐 Открыть приложение", web_app=WebAppInfo(url=web_app_url))]
])
```

## 📱 Особенности мобильной версии

### Telegram WebApp
- Автоматическая адаптация к теме Telegram
- Использование нативных кнопок Telegram (MainButton, BackButton)
- Haptic Feedback для улучшения UX
- Интеграция с облачным хранилищем Telegram

### Адаптивный дизайн
- Mobile First подход
- Touch-friendly интерфейс
- Оптимизированная навигация для мобильных
- Скрытие десктопных элементов в Telegram

## 🎨 Кастомизация

### Изменение цветовой схемы
```css
:root {
    --primary-color: #007bff;    /* Основной цвет */
    --success-color: #28a745;    /* Цвет успеха */
    --danger-color: #dc3545;     /* Цвет ошибки */
    /* ... другие переменные */
}
```

### Добавление новых страниц
1. Добавьте HTML разметку в `index.html`
2. Создайте стили в `css/components.css`
3. Добавьте логику в соответствующий JS модуль
4. Зарегистрируйте навигацию в `app.js`

### Кастомные графики
```javascript
// Создание собственного графика
chartsManager.createChart('canvas-id', {
    type: 'line',
    data: yourData,
    options: yourOptions
});
```

## 🔄 Синхронизация с ботом

### Отправка данных в бот
```javascript
// Через Telegram WebApp API
telegram.sendDataToBot({
    type: 'client_added',
    data: clientData
});
```

### Получение данных от бота
```javascript
// Обработка данных от бота
window.addEventListener('message', (event) => {
    if (event.data?.type === 'bot_data') {
        app.handleBotData(event.data);
    }
});
```

## 📈 Планы развития

- [ ] **Расширенная аналитика** - больше типов графиков
- [ ] **Планы питания** - модуль питания с калькулятором калорий
- [ ] **Система упражнений** - база упражнений с видео
- [ ] **Прогресс-фото** - загрузка и сравнение фотографий
- [ ] **Платежи** - интеграция с платежными системами
- [ ] **Групповые тренировки** - управление группами
- [ ] **Экспорт данных** - PDF отчеты, Excel файлы
- [ ] **Push-уведомления** - через Service Workers
- [ ] **Офлайн режим** - работа без интернета
- [ ] **Мультиязычность** - поддержка разных языков

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Внесите изменения и закоммитьте (`git commit -m 'Add amazing feature'`)
4. Запушьте ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 📞 Поддержка

- 📧 Email: support@example.com
- 💬 Telegram: [@your_username](https://t.me/your_username)
- 🐛 Issues: [GitHub Issues](https://github.com/bicepspshop/fitness-coach-webapp/issues)
- 📖 Wiki: [GitHub Wiki](https://github.com/bicepspshop/fitness-coach-webapp/wiki)

## 🙏 Благодарности

- [Chart.js](https://www.chartjs.org/) - за отличную библиотеку графиков
- [Font Awesome](https://fontawesome.com/) - за иконки
- [Telegram](https://core.telegram.org/bots/webapps) - за WebApp API
- Сообщество разработчиков Telegram ботов

---

**Создано с ❤️ для фитнес-тренеров**

🚀 **Начните использовать прямо сейчас**: [Открыть приложение](https://bicepspshop.github.io/fitness-coach-webapp)