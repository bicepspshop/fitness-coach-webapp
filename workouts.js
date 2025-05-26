// Модуль управления тренировками
class WorkoutsManager {
    constructor() {
        this.workouts = [];
        this.currentDate = new Date();
        this.selectedDate = null;
        this.calendarView = 'month'; // month, week, day
        
        this.initEventListeners();
    }

    initEventListeners() {
        // Добавление тренировки
        const addWorkoutBtn = document.getElementById('add-workout-btn');
        if (addWorkoutBtn) {
            addWorkoutBtn.addEventListener('click', () => {
                this.showAddWorkoutModal();
            });
        }
    }

    setWorkouts(workouts) {
        this.workouts = workouts;
        this.renderCalendar();
    }

    renderCalendar() {
        const calendar = document.getElementById('workouts-calendar');
        if (!calendar) return;

        calendar.innerHTML = `
            <div class="calendar-controls">
                <div class="calendar-nav">
                    <button class="btn btn-outline" onclick="workoutsManager.prevMonth()">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <h3>${this.getMonthYearString()}</h3>
                    <button class="btn btn-outline" onclick="workoutsManager.nextMonth()">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
                <div class="calendar-view-buttons">
                    <button class="btn ${this.calendarView === 'month' ? 'btn-primary' : 'btn-outline'}" 
                            onclick="workoutsManager.setView('month')">Месяц</button>
                    <button class="btn ${this.calendarView === 'week' ? 'btn-primary' : 'btn-outline'}" 
                            onclick="workoutsManager.setView('week')">Неделя</button>
                    <button class="btn ${this.calendarView === 'day' ? 'btn-primary' : 'btn-outline'}" 
                            onclick="workoutsManager.setView('day')">День</button>
                </div>
            </div>
            <div class="calendar-content">
                ${this.renderCalendarView()}
            </div>
        `;
    }

    renderCalendarView() {
        switch (this.calendarView) {
            case 'month':
                return this.renderMonthView();
            case 'week':
                return this.renderWeekView();
            case 'day':
                return this.renderDayView();
            default:
                return this.renderMonthView();
        }
    }

    renderMonthView() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const startDate = new Date(firstDay);
        startDate.setDate(firstDay.getDate() - firstDay.getDay() + 1); // Понедельник

        let html = `
            <div class="calendar-grid month-view">
                <div class="calendar-header">
                    ${['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map(day => 
                        `<div class="day-header">${day}</div>`
                    ).join('')}
                </div>
                <div class="calendar-body">
        `;

        const currentDate = new Date(startDate);
        for (let week = 0; week < 6; week++) {
            html += '<div class="calendar-week">';
            
            for (let day = 0; day < 7; day++) {
                const dateStr = this.formatDate(currentDate);
                const dayWorkouts = this.getWorkoutsForDate(dateStr);
                const isCurrentMonth = currentDate.getMonth() === month;
                const isToday = this.isToday(currentDate);
                
                html += `
                    <div class="calendar-day ${!isCurrentMonth ? 'other-month' : ''} ${isToday ? 'today' : ''}"
                         onclick="workoutsManager.selectDate('${dateStr}')">
                        <div class="day-number">${currentDate.getDate()}</div>
                        <div class="day-workouts">
                            ${dayWorkouts.slice(0, 3).map(workout => `
                                <div class="workout-item mini" onclick="workoutsManager.viewWorkout(${workout.id}, event)">
                                    <span class="workout-time">${workout.time}</span>
                                    <span class="workout-client">${workout.clientName}</span>
                                </div>
                            `).join('')}
                            ${dayWorkouts.length > 3 ? `<div class="more-workouts">+${dayWorkouts.length - 3}</div>` : ''}
                        </div>
                    </div>
                `;
                
                currentDate.setDate(currentDate.getDate() + 1);
            }
            
            html += '</div>';
        }

        html += '</div></div>';
        return html;
    }

    renderWeekView() {
        const startOfWeek = this.getStartOfWeek(this.currentDate);
        const days = [];
        
        for (let i = 0; i < 7; i++) {
            const date = new Date(startOfWeek);
            date.setDate(startOfWeek.getDate() + i);
            days.push(date);
        }

        let html = `
            <div class="calendar-week-view">
                <div class="week-header">
                    ${days.map(day => `
                        <div class="week-day-header ${this.isToday(day) ? 'today' : ''}">
                            <div class="day-name">${this.getDayName(day)}</div>
                            <div class="day-date">${day.getDate()}</div>
                        </div>
                    `).join('')}
                </div>
                <div class="week-body">
                    ${this.renderTimeSlots(days)}
                </div>
            </div>
        `;

        return html;
    }

    renderTimeSlots(days) {
        let html = '';
        const hours = Array.from({length: 14}, (_, i) => i + 8); // 8:00 - 21:00

        hours.forEach(hour => {
            html += `<div class="time-slot">`;
            html += `<div class="time-label">${hour}:00</div>`;
            
            days.forEach(day => {
                const dateStr = this.formatDate(day);
                const timeStr = `${hour}:00`;
                const workout = this.getWorkoutForDateTime(dateStr, timeStr);
                
                html += `
                    <div class="time-cell" data-date="${dateStr}" data-time="${timeStr}"
                         onclick="workoutsManager.scheduleAtTime('${dateStr}', '${timeStr}')">
                        ${workout ? `
                            <div class="workout-block" onclick="workoutsManager.viewWorkout(${workout.id}, event)">
                                <div class="workout-time">${workout.time}</div>
                                <div class="workout-client">${workout.clientName}</div>
                                <div class="workout-type">${workout.type}</div>
                            </div>
                        ` : ''}
                    </div>
                `;
            });
            
            html += `</div>`;
        });

        return html;
    }

    renderDayView() {
        const dayWorkouts = this.getWorkoutsForDate(this.formatDate(this.currentDate));
        
        return `
            <div class="day-view">
                <div class="day-header">
                    <h3>${this.currentDate.toLocaleDateString('ru-RU', { 
                        weekday: 'long', 
                        year: 'numeric', 
                        month: 'long', 
                        day: 'numeric' 
                    })}</h3>
                </div>
                <div class="day-workouts">
                    ${dayWorkouts.length > 0 ? dayWorkouts.map(workout => `
                        <div class="workout-card" onclick="workoutsManager.viewWorkout(${workout.id})">
                            <div class="workout-time">${workout.time}</div>
                            <div class="workout-details">
                                <h4>${workout.clientName}</h4>
                                <p>${workout.type} • ${workout.duration} мин</p>
                                <span class="workout-status ${workout.status}">${this.getStatusText(workout.status)}</span>
                            </div>
                            <div class="workout-actions">
                                <button class="btn btn-sm btn-primary" onclick="workoutsManager.editWorkout(${workout.id}, event)">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-success" onclick="workoutsManager.completeWorkout(${workout.id}, event)">
                                    <i class="fas fa-check"></i>
                                </button>
                            </div>
                        </div>
                    `).join('') : `
                        <div class="empty-day">
                            <i class="fas fa-calendar-plus fa-3x"></i>
                            <h3>Нет запланированных тренировок</h3>
                            <button class="btn btn-primary" onclick="workoutsManager.showAddWorkoutModal()">
                                Запланировать тренировку
                            </button>
                        </div>
                    `}
                </div>
            </div>
        `;
    }

    // Вспомогательные методы
    getWorkoutsForDate(dateStr) {
        return this.workouts.filter(workout => workout.date === dateStr);
    }

    getWorkoutForDateTime(dateStr, timeStr) {
        return this.workouts.find(workout => 
            workout.date === dateStr && workout.time === timeStr
        );
    }

    formatDate(date) {
        return date.toISOString().split('T')[0];
    }

    isToday(date) {
        const today = new Date();
        return date.toDateString() === today.toDateString();
    }

    getStartOfWeek(date) {
        const d = new Date(date);
        const day = d.getDay();
        const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Понедельник
        return new Date(d.setDate(diff));
    }

    getDayName(date) {
        return date.toLocaleDateString('ru-RU', { weekday: 'short' });
    }

    getMonthYearString() {
        return this.currentDate.toLocaleDateString('ru-RU', { 
            year: 'numeric', 
            month: 'long' 
        });
    }

    getStatusText(status) {
        const statusMap = {
            'scheduled': 'Запланирована',
            'completed': 'Завершена',
            'cancelled': 'Отменена',
            'in-progress': 'В процессе'
        };
        return statusMap[status] || status;
    }

    // Навигация по календарю
    prevMonth() {
        this.currentDate.setMonth(this.currentDate.getMonth() - 1);
        this.renderCalendar();
    }

    nextMonth() {
        this.currentDate.setMonth(this.currentDate.getMonth() + 1);
        this.renderCalendar();
    }

    setView(view) {
        this.calendarView = view;
        this.renderCalendar();
    }

    selectDate(dateStr) {
        this.selectedDate = dateStr;
        this.currentDate = new Date(dateStr);
        this.setView('day');
    }

    // Действия с тренировками
    showAddWorkoutModal() {
        if (window.app) {
            window.app.showAddWorkoutModal();
        }
    }

    scheduleAtTime(dateStr, timeStr) {
        if (window.app) {
            window.app.scheduleWorkout(null, dateStr, timeStr);
        }
    }

    viewWorkout(workoutId, event) {
        if (event) event.stopPropagation();
        
        const workout = this.workouts.find(w => w.id === workoutId);
        if (workout && window.app) {
            window.app.viewWorkout(workout);
        }
    }

    editWorkout(workoutId, event) {
        if (event) event.stopPropagation();
        
        if (window.app) {
            window.app.editWorkout(workoutId);
        }
    }

    completeWorkout(workoutId, event) {
        if (event) event.stopPropagation();
        
        if (window.app) {
            window.app.completeWorkout(workoutId);
        }
    }
}

// Создаем глобальный экземпляр
window.workoutsManager = new WorkoutsManager();
