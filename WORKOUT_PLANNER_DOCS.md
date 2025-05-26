# 🏋️‍♀️ Планировщик тренировок - Документация

## Обзор

Планировщик тренировок - это веб-приложение для создания детальных планов тренировок с функционалом:
- Пошаговое создание тренировки
- База упражнений по категориям
- Настройка параметров упражнений
- Шаблоны тренировок
- Drag & Drop для изменения порядка
- Интеграция с Telegram WebApp

## Структура файлов

```
web/
├── workout-planner.html    # Страница планировщика
├── js/
│   └── workout-planner.js  # Основная логика планировщика
├── css/
│   ├── style.css          # Основные стили
│   └── components.css     # Компоненты UI
└── index.html             # Главная страница (обновлена)
```

## Использование

### 1. Запуск планировщика

Из главного приложения:
```javascript
// Кнопка "Планировщик тренировок" 
app.openWorkoutPlanner()
```

Прямая ссылка:
```html
<a href="workout-planner.html">Открыть планировщик</a>
```

### 2. Процесс создания тренировки

#### Шаг 1: Информация о тренировке
- Выбор клиента
- Дата и время
- Тип тренировки
- Длительность
- Место проведения

#### Шаг 2: Выбор упражнений
- 6 категорий упражнений
- Готовые шаблоны тренировок
- Добавление в план кликом
- Базовые параметры сразу в плане

#### Шаг 3: Настройка параметров
- Подходы и повторения
- Вес (опционально)
- Время отдыха
- Заметки к упражнениям

#### Шаг 4: Сохранение
- Итоговая сводка
- Статистика тренировки
- Сохранение в localStorage

## API класса WorkoutPlanner

### Создание тренировки
```javascript
const planner = new WorkoutPlanner();

// Создать новую тренировку
planner.createWorkout(
    clientId,    // ID клиента
    date,        // Дата (YYYY-MM-DD)
    time,        // Время (HH:MM)
    type,        // Тип: strength, cardio, functional, stretching, mixed
    duration,    // Длительность в минутах
    location     // Место проведения
);
```

### Работа с упражнениями
```javascript
// Добавить упражнение в план
planner.addExerciseToWorkout(
    exerciseId,  // ID упражнения
    sets,        // Количество подходов
    reps,        // Повторения (строка, например "10-12")
    weight,      // Вес в кг (опционально)
    rest,        // Отдых в секундах
    notes        // Заметки
);

// Удалить упражнение
planner.removeExerciseFromWorkout(index);

// Изменить порядок
planner.reorderExercises(fromIndex, toIndex);
```

### Получение данных
```javascript
// Тренировки клиента
const clientWorkouts = planner.getClientWorkouts(clientId);

// Тренировки на дату
const todayWorkouts = planner.getWorkoutsByDate('2024-12-25');

// Предстоящие тренировки
const upcoming = planner.getUpcomingWorkouts(10);

// Статистика
const stats = planner.getStatistics();
```

### Шаблоны тренировок
```javascript
// Загрузить шаблон
const template = planner.generateWorkoutTemplate('strength', 'beginner');

// Применить шаблон
planner.loadTemplate('cardio', 'intermediate');
```

## База упражнений

### Категории
- **chest** - Упражнения для груди
- **back** - Упражнения для спины
- **legs** - Упражнения для ног
- **arms** - Упражнения для рук
- **cardio** - Кардио упражнения
- **stretching** - Растяжка

### Структура упражнения
```javascript
{
    id: 1,
    name: 'Жим лежа',
    category: 'chest',
    equipment: 'штанга',
    difficulty: 'intermediate'
}
```

## Интеграция с Telegram

### Инициализация
```javascript
if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();
    
    // Кнопка "Назад"
    tg.BackButton.show();
}
```

### Отправка данных
```javascript
// После сохранения тренировки
window.Telegram.WebApp.sendData(JSON.stringify({
    action: 'workout_created',
    workout: workoutData
}));
```

## Хранение данных

Все данные сохраняются в localStorage:
- **workouts** - Массив всех тренировок
- **fitnessClients** - Список клиентов

### Формат тренировки
```javascript
{
    id: 1703500000000,
    clientId: 1,
    date: '2024-12-25',
    time: '10:00',
    type: 'strength',
    duration: 60,
    location: 'Зал №1',
    exercises: [
        {
            id: 1,
            name: 'Жим лежа',
            category: 'chest',
            sets: 4,
            reps: '8-10',
            weight: '80',
            rest: 90,
            notes: 'Следить за техникой',
            order: 1
        }
    ],
    status: 'planned',
    createdAt: '2024-12-25T08:00:00.000Z'
}
```

## Стилизация

### CSS переменные
```css
:root {
    --primary-color: #007bff;
    --bg-color: #ffffff;
    --text-color: #212529;
    --secondary-bg: #f8f9fa;
    --hint-color: #6c757d;
}
```

### Темная тема
Автоматически применяется через `@media (prefers-color-scheme: dark)`

## События

### Пользовательские события
```javascript
// Тренировка сохранена
window.addEventListener('workoutSaved', (e) => {
    console.log('Сохранена тренировка:', e.detail);
});

// Тренировка удалена
window.addEventListener('workoutDeleted', (e) => {
    console.log('Удалена тренировка:', e.detail.workoutId);
});
```

## Расширение функционала

### Добавление новых упражнений
```javascript
// В методе loadExercises()
shoulders: [
    { 
        id: 31, 
        name: 'Жим стоя', 
        category: 'shoulders', 
        equipment: 'штанга', 
        difficulty: 'intermediate' 
    }
]
```

### Новые типы тренировок
```html
<option value="yoga">Йога</option>
<option value="pilates">Пилатес</option>
```

### Кастомные шаблоны
```javascript
planner.customTemplates = {
    fullBody: [
        { exerciseId: 1, sets: 3, reps: '10' },
        { exerciseId: 11, sets: 3, reps: '12' },
        { exerciseId: 6, sets: 3, reps: '8' }
    ]
};
```

## Примеры использования

### Создание тренировки с шаблоном
```javascript
// Инициализация
const planner = new WorkoutPlanner();

// Создание тренировки
planner.createWorkout(1, '2024-12-25', '10:00', 'strength', 60, 'Зал №1');

// Загрузка шаблона
planner.loadTemplate('strength', 'beginner');

// Сохранение
planner.saveWorkout();
```

### Копирование тренировки
```javascript
// Копировать тренировку на завтра
const tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);

const newWorkout = planner.copyWorkout(
    workoutId, 
    tomorrow.toISOString().split('T')[0],
    '11:00'
);
```

## Оптимизация

- Ленивая загрузка упражнений
- Кеширование данных в памяти
- Минимизация перерисовок DOM
- Debounce для поисковых запросов

## Безопасность

- Валидация всех вводимых данных
- Экранирование HTML в пользовательском контенте
- Ограничение размера сохраняемых данных
- HTTPS для Telegram WebApp

## Поддержка браузеров

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+
- Мобильные браузеры (iOS Safari, Chrome Android)

## Известные проблемы

1. **localStorage в приватном режиме** - Данные не сохраняются
2. **Drag & Drop на мобильных** - Используйте кнопки перемещения
3. **Telegram WebApp ограничения** - Максимум 4KB для sendData

## Дальнейшее развитие

- [ ] Синхронизация с сервером
- [ ] Экспорт в PDF
- [ ] Видео упражнений
- [ ] Таймер для тренировки
- [ ] История изменений
- [ ] Общие шаблоны между тренерами
