// Модуль планирования тренировок
class WorkoutPlanner {
    constructor() {
        this.workouts = this.loadWorkouts();
        this.exercises = this.loadExercises();
        this.currentWorkout = null;
        this.selectedExercises = [];
    }

    // Загрузка данных
    loadWorkouts() {
        const saved = localStorage.getItem('workouts');
        return saved ? JSON.parse(saved) : [];
    }

    loadExercises() {
        // Базовая база упражнений
        return {
            chest: [
                { id: 1, name: 'Жим лежа', category: 'chest', equipment: 'штанга', difficulty: 'intermediate' },
                { id: 2, name: 'Отжимания', category: 'chest', equipment: 'без оборудования', difficulty: 'beginner' },
                { id: 3, name: 'Жим гантелей', category: 'chest', equipment: 'гантели', difficulty: 'intermediate' },
                { id: 4, name: 'Разводка гантелей', category: 'chest', equipment: 'гантели', difficulty: 'intermediate' },
                { id: 5, name: 'Отжимания на брусьях', category: 'chest', equipment: 'брусья', difficulty: 'intermediate' }
            ],
            back: [
                { id: 6, name: 'Подтягивания', category: 'back', equipment: 'турник', difficulty: 'intermediate' },
                { id: 7, name: 'Тяга штанги в наклоне', category: 'back', equipment: 'штанга', difficulty: 'intermediate' },
                { id: 8, name: 'Тяга верхнего блока', category: 'back', equipment: 'тренажер', difficulty: 'beginner' },
                { id: 9, name: 'Гиперэкстензия', category: 'back', equipment: 'тренажер', difficulty: 'beginner' },
                { id: 10, name: 'Тяга гантели в наклоне', category: 'back', equipment: 'гантели', difficulty: 'intermediate' }
            ],
            legs: [
                { id: 11, name: 'Приседания со штангой', category: 'legs', equipment: 'штанга', difficulty: 'intermediate' },
                { id: 12, name: 'Приседания без веса', category: 'legs', equipment: 'без оборудования', difficulty: 'beginner' },
                { id: 13, name: 'Выпады', category: 'legs', equipment: 'без оборудования', difficulty: 'beginner' },
                { id: 14, name: 'Жим ногами', category: 'legs', equipment: 'тренажер', difficulty: 'beginner' },
                { id: 15, name: 'Подъемы на икры', category: 'legs', equipment: 'без оборудования', difficulty: 'beginner' }
            ],
            arms: [
                { id: 16, name: 'Подъем штанги на бицепс', category: 'arms', equipment: 'штанга', difficulty: 'beginner' },
                { id: 17, name: 'Французский жим', category: 'arms', equipment: 'штанга', difficulty: 'intermediate' },
                { id: 18, name: 'Молотки', category: 'arms', equipment: 'гантели', difficulty: 'beginner' },
                { id: 19, name: 'Отжимания узким хватом', category: 'arms', equipment: 'без оборудования', difficulty: 'intermediate' },
                { id: 20, name: 'Подъем гантелей на бицепс', category: 'arms', equipment: 'гантели', difficulty: 'beginner' }
            ],
            cardio: [
                { id: 21, name: 'Бег', category: 'cardio', equipment: 'без оборудования', difficulty: 'beginner' },
                { id: 22, name: 'Берпи', category: 'cardio', equipment: 'без оборудования', difficulty: 'intermediate' },
                { id: 23, name: 'Прыжки на скакалке', category: 'cardio', equipment: 'скакалка', difficulty: 'beginner' },
                { id: 24, name: 'Велотренажер', category: 'cardio', equipment: 'тренажер', difficulty: 'beginner' },
                { id: 25, name: 'Эллиптический тренажер', category: 'cardio', equipment: 'тренажер', difficulty: 'beginner' }
            ],
            stretching: [
                { id: 26, name: 'Растяжка спины', category: 'stretching', equipment: 'без оборудования', difficulty: 'beginner' },
                { id: 27, name: 'Растяжка ног', category: 'stretching', equipment: 'без оборудования', difficulty: 'beginner' },
                { id: 28, name: 'Планка', category: 'stretching', equipment: 'без оборудования', difficulty: 'beginner' },
                { id: 29, name: 'Растяжка плеч', category: 'stretching', equipment: 'без оборудования', difficulty: 'beginner' },
                { id: 30, name: 'Йога-комплекс', category: 'stretching', equipment: 'коврик', difficulty: 'intermediate' }
            ]
        };
    }

    // Создание тренировки
    createWorkout(clientId, date, time, type, duration, location) {
        const workout = {
            id: Date.now(),
            clientId,
            date,
            time,
            type,
            duration,
            location,
            exercises: [],
            status: 'planned',
            createdAt: new Date().toISOString()
        };
        
        this.currentWorkout = workout;
        this.selectedExercises = [];
        return workout;
    }

    // Добавление упражнения в план
    addExerciseToWorkout(exerciseId, sets, reps, weight, rest, notes) {
        const exercise = this.findExerciseById(exerciseId);
        if (!exercise) return false;

        const workoutExercise = {
            id: exerciseId,
            name: exercise.name,
            category: exercise.category,
            sets: parseInt(sets),
            reps: reps,
            weight: weight || null,
            rest: rest || 60,
            notes: notes || '',
            order: this.selectedExercises.length + 1
        };

        this.selectedExercises.push(workoutExercise);
        return true;
    }

    // Удаление упражнения из плана
    removeExerciseFromWorkout(index) {
        this.selectedExercises.splice(index, 1);
        // Пересчитываем порядок
        this.selectedExercises.forEach((ex, i) => {
            ex.order = i + 1;
        });
    }

    // Изменение порядка упражнений
    reorderExercises(fromIndex, toIndex) {
        const [removed] = this.selectedExercises.splice(fromIndex, 1);
        this.selectedExercises.splice(toIndex, 0, removed);
        // Пересчитываем порядок
        this.selectedExercises.forEach((ex, i) => {
            ex.order = i + 1;
        });
    }

    // Сохранение тренировки
    saveWorkout() {
        if (!this.currentWorkout) return false;
        
        this.currentWorkout.exercises = [...this.selectedExercises];
        this.workouts.push(this.currentWorkout);
        
        // Сохраняем в localStorage
        localStorage.setItem('workouts', JSON.stringify(this.workouts));
        
        // Отправляем событие для обновления UI
        window.dispatchEvent(new CustomEvent('workoutSaved', { 
            detail: this.currentWorkout 
        }));
        
        // Очищаем текущую тренировку
        this.currentWorkout = null;
        this.selectedExercises = [];
        
        return true;
    }

    // Получение тренировок клиента
    getClientWorkouts(clientId) {
        return this.workouts.filter(w => w.clientId === clientId)
            .sort((a, b) => new Date(b.date + ' ' + b.time) - new Date(a.date + ' ' + a.time));
    }

    // Получение тренировок на дату
    getWorkoutsByDate(date) {
        return this.workouts.filter(w => w.date === date)
            .sort((a, b) => a.time.localeCompare(b.time));
    }

    // Получение предстоящих тренировок
    getUpcomingWorkouts(limit = 10) {
        const now = new Date();
        return this.workouts
            .filter(w => {
                const workoutDate = new Date(w.date + ' ' + w.time);
                return workoutDate > now && w.status === 'planned';
            })
            .sort((a, b) => {
                const dateA = new Date(a.date + ' ' + a.time);
                const dateB = new Date(b.date + ' ' + b.time);
                return dateA - dateB;
            })
            .slice(0, limit);
    }

    // Поиск упражнения по ID
    findExerciseById(id) {
        for (const category in this.exercises) {
            const exercise = this.exercises[category].find(e => e.id === id);
            if (exercise) return exercise;
        }
        return null;
    }

    // Получение упражнений по категории
    getExercisesByCategory(category) {
        return this.exercises[category] || [];
    }

    // Копирование тренировки
    copyWorkout(workoutId, newDate, newTime) {
        const original = this.workouts.find(w => w.id === workoutId);
        if (!original) return null;

        const copy = {
            ...original,
            id: Date.now(),
            date: newDate,
            time: newTime,
            status: 'planned',
            createdAt: new Date().toISOString(),
            exercises: original.exercises.map(ex => ({...ex}))
        };

        this.workouts.push(copy);
        localStorage.setItem('workouts', JSON.stringify(this.workouts));
        
        return copy;
    }

    // Обновление статуса тренировки
    updateWorkoutStatus(workoutId, status) {
        const workout = this.workouts.find(w => w.id === workoutId);
        if (!workout) return false;

        workout.status = status;
        if (status === 'completed') {
            workout.completedAt = new Date().toISOString();
        }

        localStorage.setItem('workouts', JSON.stringify(this.workouts));
        return true;
    }

    // Удаление тренировки
    deleteWorkout(workoutId) {
        const index = this.workouts.findIndex(w => w.id === workoutId);
        if (index === -1) return false;

        this.workouts.splice(index, 1);
        localStorage.setItem('workouts', JSON.stringify(this.workouts));
        
        window.dispatchEvent(new CustomEvent('workoutDeleted', { 
            detail: { workoutId } 
        }));
        
        return true;
    }

    // Получение статистики
    getStatistics() {
        const stats = {
            total: this.workouts.length,
            planned: this.workouts.filter(w => w.status === 'planned').length,
            completed: this.workouts.filter(w => w.status === 'completed').length,
            cancelled: this.workouts.filter(w => w.status === 'cancelled').length,
            
            // По типам тренировок
            byType: {},
            
            // По клиентам
            byClient: {},
            
            // Самые популярные упражнения
            popularExercises: {}
        };

        // Подсчет по типам
        this.workouts.forEach(workout => {
            stats.byType[workout.type] = (stats.byType[workout.type] || 0) + 1;
            stats.byClient[workout.clientId] = (stats.byClient[workout.clientId] || 0) + 1;
            
            // Подсчет упражнений
            workout.exercises.forEach(exercise => {
                stats.popularExercises[exercise.name] = (stats.popularExercises[exercise.name] || 0) + 1;
            });
        });

        // Сортировка популярных упражнений
        stats.topExercises = Object.entries(stats.popularExercises)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([name, count]) => ({ name, count }));

        return stats;
    }

    // Генерация шаблонов тренировок
    generateWorkoutTemplate(type, level = 'beginner') {
        const templates = {
            strength: {
                beginner: [
                    { exerciseId: 2, sets: 3, reps: '10-12' },  // Отжимания
                    { exerciseId: 12, sets: 3, reps: '15' },    // Приседания
                    { exerciseId: 8, sets: 3, reps: '12' },     // Тяга верхнего блока
                    { exerciseId: 28, sets: 3, reps: '30 сек' } // Планка
                ],
                intermediate: [
                    { exerciseId: 1, sets: 4, reps: '8-10' },   // Жим лежа
                    { exerciseId: 11, sets: 4, reps: '10-12' }, // Приседания со штангой
                    { exerciseId: 7, sets: 4, reps: '10' },     // Тяга штанги
                    { exerciseId: 16, sets: 3, reps: '12' }     // Подъем на бицепс
                ]
            },
            cardio: {
                beginner: [
                    { exerciseId: 21, sets: 1, reps: '20 мин' }, // Бег
                    { exerciseId: 22, sets: 3, reps: '10' },     // Берпи
                    { exerciseId: 23, sets: 3, reps: '100' }     // Скакалка
                ],
                intermediate: [
                    { exerciseId: 21, sets: 1, reps: '30 мин' }, // Бег
                    { exerciseId: 22, sets: 5, reps: '15' },     // Берпи
                    { exerciseId: 24, sets: 1, reps: '20 мин' }  // Велотренажер
                ]
            }
        };

        return templates[type]?.[level] || [];
    }
}

// Экспортируем класс для использования
window.WorkoutPlanner = WorkoutPlanner;
