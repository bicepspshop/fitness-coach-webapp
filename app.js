// Главное приложение фитнес-помощника
class FitnessApp {
    constructor() {
        this.currentPage = 'dashboard';
        this.data = {
            trainer: {
                name: 'Фитнес Тренер',
                clients: 25,
                workouts: 156,
                revenue: 127500
            },
            clients: [
                { 
                    id: 1, 
                    name: 'Анна Иванова', 
                    avatar: 'АИ',
                    goal: 'Похудение', 
                    progress: 75, 
                    isActive: true,
                    email: 'anna@example.com',
                    phone: '+7 999 123 45 67',
                    nextWorkout: '2024-05-27'
                },
                { 
                    id: 2, 
                    name: 'Петр Сидоров', 
                    avatar: 'ПС',
                    goal: 'Набор массы', 
                    progress: 60, 
                    isActive: true,
                    email: 'petr@example.com',
                    phone: '+7 999 123 45 68',
                    nextWorkout: '2024-05-26'
                },
                { 
                    id: 3, 
                    name: 'Мария Петрова', 
                    avatar: 'МП',
                    goal: 'Поддержание формы', 
                    progress: 85, 
                    isActive: true,
                    email: 'maria@example.com',
                    phone: '+7 999 123 45 69',
                    nextWorkout: '2024-05-28'
                }
            ],
            workouts: [
                {
                    id: 1,
                    clientId: 1,
                    clientName: 'Анна Иванова',
                    date: '2024-05-26',
                    time: '09:00',
                    duration: 60,
                    type: 'strength',
                    status: 'scheduled',
                    location: 'Спортзал'
                },
                {
                    id: 2,
                    clientId: 2,
                    clientName: 'Петр Сидоров',
                    date: '2024-05-26',
                    time: '11:00',
                    duration: 60,
                    type: 'cardio',
                    status: 'completed',
                    location: 'Спортзал'
                },
                {
                    id: 3,
                    clientId: 3,
                    clientName: 'Мария Петрова',
                    date: '2024-05-26',
                    time: '14:00',
                    duration: 60,
                    type: 'functional',
                    status: 'scheduled',
                    location: 'Спортзал'
                }
            ]
        };
        
        this.init();
    }

    init() {
        console.log('Инициализация приложения...');
        
        // Инициализация Telegram WebApp
        if (window.telegramIntegration) {
            this.telegram = window.telegramIntegration;
        }
        
        this.bindEvents();
        this.updateStats();
        this.renderTodaySchedule();
        
        // Инициализируем менеджеры
        if (window.clientsManager) {
            window.clientsManager.setClients(this.data.clients);
        }
        
        if (window.workoutsManager) {
            window.workoutsManager.setWorkouts(this.data.workouts);
        }
        
        setTimeout(() => {
            this.hideLoader();
            this.initDashboardChart();
        }, 1000);
    }

    bindEvents() {
        // Навигация
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = link.getAttribute('data-page');
                this.navigateTo(page);
            });
        });

        // Мобильное меню
        const menuToggle = document.getElementById('menu-toggle');
        if (menuToggle) {
            menuToggle.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }

        // Быстрые действия
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const onclick = btn.getAttribute('onclick');
                if (onclick) {
                    eval(onclick);
                }
            });
        });

        // Уведомления
        document.getElementById('notifications-btn')?.addEventListener('click', () => {
            this.showNotification('У вас 3 новых уведомления', 'info');
        });

        // Формы
        this.bindFormEvents();

        // Обработчик для закрытия модалок по клику вне них
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-overlay')) {
                const modalId = e.target.id;
                this.closeModal(modalId);
            }
        });

        // Поиск клиентов
        const searchInput = document.getElementById('clients-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.handleClientSearch(e.target.value);
            });
        }
    }

    bindFormEvents() {
        // Форма добавления клиента
        const addClientForm = document.getElementById('add-client-form');
        if (addClientForm) {
            addClientForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleAddClient(new FormData(addClientForm));
            });
        }

        // Форма добавления тренировки
        const addWorkoutForm = document.getElementById('add-workout-form');
        if (addWorkoutForm) {
            addWorkoutForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleAddWorkout(new FormData(addWorkoutForm));
            });
        }
    }

    navigateTo(page) {
        // Скрываем все страницы
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        
        // Показываем нужную страницу
        const targetPage = document.getElementById(`${page}-page`);
        if (targetPage) {
            targetPage.classList.add('active');
            this.currentPage = page;
            
            // Эмитируем событие для других модулей
            document.dispatchEvent(new CustomEvent('pageChanged', { 
                detail: { page } 
            }));
        }

        // Обновляем навигацию
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('data-page') === page) {
                link.classList.add('active');
            }
        });

        // Загружаем данные для страницы
        this.loadPageData(page);

        // Закрываем мобильное меню
        if (window.innerWidth <= 1024) {
            document.getElementById('sidebar')?.classList.remove('show');
        }

        // Вибрация при переключении
        if (this.telegram) {
            this.telegram.hapticFeedback('selection');
        }
    }

    loadPageData(page) {
        switch (page) {
            case 'clients':
                if (window.clientsManager) {
                    window.clientsManager.setClients(this.data.clients);
                }
                break;
            case 'workouts':
                if (window.workoutsManager) {
                    window.workoutsManager.setWorkouts(this.data.workouts);
                }
                break;
            case 'analytics':
                setTimeout(() => this.initAnalyticsCharts(), 100);
                break;
        }
    }

    toggleSidebar() {
        document.getElementById('sidebar')?.classList.toggle('show');
    }

    hideLoader() {
        document.getElementById('loader').style.display = 'none';
        document.getElementById('app').style.display = 'block';
    }

    updateStats() {
        const stats = this.data.trainer;
        const totalClientsEl = document.getElementById('total-clients');
        const totalWorkoutsEl = document.getElementById('total-workouts');
        const totalRevenueEl = document.getElementById('total-revenue');
        const todayWorkoutsEl = document.getElementById('today-workouts');

        if (totalClientsEl) totalClientsEl.textContent = stats.clients;
        if (totalWorkoutsEl) totalWorkoutsEl.textContent = stats.workouts;
        if (totalRevenueEl) totalRevenueEl.textContent = stats.revenue.toLocaleString() + '₽';
        if (todayWorkoutsEl) todayWorkoutsEl.textContent = '5';
    }

    renderTodaySchedule() {
        const scheduleContainer = document.getElementById('today-schedule');
        if (!scheduleContainer) return;

        const today = new Date().toISOString().split('T')[0];
        const todayWorkouts = this.data.workouts.filter(w => w.date === today);

        if (todayWorkouts.length === 0) {
            scheduleContainer.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-calendar-day"></i>
                    <p>На сегодня тренировок не запланировано</p>
                </div>
            `;
            return;
        }

        scheduleContainer.innerHTML = todayWorkouts.map(workout => `
            <div class="schedule-item">
                <div class="schedule-time">${workout.time}</div>
                <div class="schedule-info">
                    <strong>${workout.clientName}</strong>
                    <span>${this.getWorkoutTypeText(workout.type)} • ${workout.duration} мин</span>
                </div>
                <div class="schedule-status ${workout.status}">
                    ${this.getStatusText(workout.status)}
                </div>
            </div>
        `).join('');
    }

    getWorkoutTypeText(type) {
        const types = {
            'strength': 'Силовая',
            'cardio': 'Кардио',
            'functional': 'Функциональная',
            'stretching': 'Растяжка',
            'mixed': 'Смешанная'
        };
        return types[type] || type;
    }

    getStatusText(status) {
        const statuses = {
            'scheduled': 'Запланирована',
            'completed': 'Завершена',
            'cancelled': 'Отменена',
            'in-progress': 'В процессе'
        };
        return statuses[status] || status;
    }

    // Модальные окна
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
            
            // Эмитируем событие
            document.dispatchEvent(new CustomEvent('modalOpened', { 
                detail: { modalId, type: 'form' } 
            }));
        }
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('show');
            document.body.style.overflow = '';
            
            // Очищаем формы
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
            }
            
            // Эмитируем событие
            document.dispatchEvent(new CustomEvent('modalClosed', { 
                detail: { modalId } 
            }));
        }
    }

    showAddClientModal() {
        this.showModal('add-client-modal');
    }

    showAddWorkoutModal() {
        this.showModal('add-workout-modal');
    }

    showAddNutritionModal() {
        this.showNotification('Функция планов питания в разработке', 'info');
    }

    showAddPaymentModal() {
        this.showNotification('Функция учета платежей в разработке', 'info');
    }

    showHelp() {
        this.showNotification('Если у вас есть вопросы, обратитесь к администратору', 'info');
    }

    // Обработчики форм
    handleAddClient(formData) {
        const clientData = {
            id: this.data.clients.length + 1,
            name: `${formData.get('firstName')} ${formData.get('lastName') || ''}`.trim(),
            avatar: this.getInitials(`${formData.get('firstName')} ${formData.get('lastName') || ''}`),
            email: formData.get('email'),
            phone: formData.get('phone'),
            goal: this.getGoalText(formData.get('goal')),
            progress: 0,
            isActive: true,
            nextWorkout: null
        };

        this.data.clients.push(clientData);
        
        if (window.clientsManager) {
            window.clientsManager.setClients(this.data.clients);
        }

        this.closeModal('add-client-modal');
        this.showNotification(`Клиент "${clientData.name}" успешно добавлен!`, 'success');
        
        // Обновляем статистику
        this.data.trainer.clients = this.data.clients.length;
        this.updateStats();

        // Эмитируем событие
        document.dispatchEvent(new CustomEvent('clientAdded', { 
            detail: clientData 
        }));

        // Переходим на страницу клиентов
        this.navigateTo('clients');
    }

    handleAddWorkout(formData) {
        const workoutData = {
            id: this.data.workouts.length + 1,
            clientId: parseInt(formData.get('clientId')),
            clientName: this.getClientName(parseInt(formData.get('clientId'))),
            date: formData.get('date'),
            time: formData.get('time'),
            duration: parseInt(formData.get('duration')),
            type: formData.get('type'),
            status: 'scheduled',
            location: formData.get('location'),
            notes: formData.get('notes')
        };

        this.data.workouts.push(workoutData);
        
        if (window.workoutsManager) {
            window.workoutsManager.setWorkouts(this.data.workouts);
        }

        this.closeModal('add-workout-modal');
        this.showNotification(`Тренировка для ${workoutData.clientName} запланирована!`, 'success');
        
        // Обновляем расписание на сегодня
        this.renderTodaySchedule();

        // Эмитируем событие
        document.dispatchEvent(new CustomEvent('workoutScheduled', { 
            detail: workoutData 
        }));

        // Переходим на страницу тренировок
        this.navigateTo('workouts');
    }

    getClientName(clientId) {
        const client = this.data.clients.find(c => c.id === clientId);
        return client ? client.name : 'Неизвестный клиент';
    }

    getGoalText(goal) {
        const goals = {
            'weight_loss': 'Похудение',
            'muscle_gain': 'Набор массы',
            'strength': 'Увеличение силы',
            'endurance': 'Развитие выносливости',
            'health': 'Общее оздоровление',
            'sport_specific': 'Спортивная подготовка'
        };
        return goals[goal] || 'Не указана';
    }

    getInitials(name) {
        return name.split(' ')
            .map(n => n[0])
            .join('')
            .toUpperCase()
            .substring(0, 2);
    }

    // Поиск клиентов
    handleClientSearch(query) {
        if (window.clientsManager) {
            window.clientsManager.searchTerm = query.toLowerCase();
            window.clientsManager.filterAndRenderClients();
        }
    }

    // Действия с клиентами
    viewClient(clientId) {
        const client = this.data.clients.find(c => c.id === clientId);
        if (client) {
            this.showNotification(`Просмотр клиента: ${client.name}`, 'info');
            
            if (this.telegram) {
                this.telegram.hapticFeedback('impact', 'light');
            }
        }
    }

    scheduleWorkout(clientId, date = null, time = null) {
        this.showAddWorkoutModal();
        
        // Предзаполняем форму если переданы параметры
        setTimeout(() => {
            if (clientId) {
                const clientSelect = document.querySelector('#add-workout-modal select[name="clientId"]');
                if (clientSelect) {
                    clientSelect.value = clientId;
                }
            }
            
            if (date) {
                const dateInput = document.querySelector('#add-workout-modal input[name="date"]');
                if (dateInput) {
                    dateInput.value = date;
                }
            }
            
            if (time) {
                const timeInput = document.querySelector('#add-workout-modal input[name="time"]');
                if (timeInput) {
                    timeInput.value = time;
                }
            }
        }, 100);
    }

    viewWorkout(workout) {
        this.showNotification(`Тренировка: ${workout.clientName} в ${workout.time}`, 'info');
    }

    editWorkout(workoutId) {
        this.showNotification(`Редактирование тренировки #${workoutId}`, 'info');
    }

    completeWorkout(workoutId) {
        const workout = this.data.workouts.find(w => w.id === workoutId);
        if (workout) {
            workout.status = 'completed';
            this.showNotification(`Тренировка с ${workout.clientName} отмечена как завершенная`, 'success');
            this.renderTodaySchedule();
            
            if (window.workoutsManager) {
                window.workoutsManager.setWorkouts(this.data.workouts);
            }
        }
    }

    // Уведомления
    showNotification(message, type = 'info') {
        // Используем Telegram уведомления если доступно
        if (this.telegram) {
            this.telegram.showAlert(message);
            return;
        }

        // Fallback для браузера
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}-circle"></i>
            <span>${message}</span>
        `;

        // Контейнер для уведомлений
        let container = document.querySelector('.notification-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'notification-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 3000;
                display: flex;
                flex-direction: column;
                gap: 10px;
            `;
            document.body.appendChild(container);
        }

        notification.style.cssText = `
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: white;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            min-width: 300px;
            animation: slideIn 0.3s ease;
            background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;

        container.appendChild(notification);

        // Удаляем через 3 секунды
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Графики
    initDashboardChart() {
        if (window.ChartsManager) {
            const chartsManager = new window.ChartsManager();
            chartsManager.createProgressChart('progressChart', this.data.clients);
        }
    }

    initAnalyticsCharts() {
        if (!window.ChartsManager) return;
        
        const chartsManager = new window.ChartsManager();
        
        setTimeout(() => {
            // График новых клиентов
            chartsManager.createClientAcquisitionChart('clientsChart', this.data.clients);
            
            // График доходов
            chartsManager.createRevenueChart('revenueChart');
            
            // График типов тренировок
            chartsManager.createWorkoutDistributionChart('workoutTypesChart', this.data.workouts);
            
            // График посещаемости
            chartsManager.createAttendanceChart('attendanceChart', {
                scheduled: [15, 18, 16, 20],
                attended: [14, 16, 15, 18],
                missed: [1, 2, 1, 2]
            });
        }, 100);
    }
}

// Инициализация при загрузке DOM
let app;

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM загружен, инициализируем приложение...');
    
    // Небольшая задержка для загрузки всех ресурсов
    setTimeout(() => {
        app = new FitnessApp();
        console.log('Приложение инициализировано');
    }, 500);
});

// Стили для уведомлений
const styles = document.createElement('style');
styles.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .empty-state {
        text-align: center;
        padding: 2rem;
        color: var(--text-secondary);
    }
    
    .empty-state i {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
`;
document.head.appendChild(styles);