// Главный файл приложения
class FitnessApp {
    constructor() {
        this.currentPage = 'dashboard';
        this.isLoading = false;
        this.data = {
            trainer: null,
            clients: [],
            workouts: [],
            programs: []
        };
        
        this.init();
    }

    async init() {
        // Показываем лоадер
        this.showLoader();
        
        // Инициализируем Telegram Web App
        this.initTelegram();
        
        // Загружаем данные
        await this.loadData();
        
        // Инициализируем компоненты
        this.initComponents();
        
        // Привязываем события
        this.bindEvents();
        
        // Скрываем лоадер и показываем приложение
        this.hideLoader();
        
        // Инициализируем графики
        this.initCharts();
    }

    initTelegram() {
        if (window.Telegram?.WebApp) {
            const tg = window.Telegram.WebApp;
            
            // Настраиваем тему
            document.documentElement.style.setProperty('--primary-color', tg.themeParams.button_color || '#007bff');
            document.documentElement.style.setProperty('--bg-color', tg.themeParams.bg_color || '#ffffff');
            document.documentElement.style.setProperty('--text-color', tg.themeParams.text_color || '#212529');
            
            // Расширяем приложение
            tg.expand();
            
            // Настраиваем главную кнопку
            tg.MainButton.setText('Сохранить');
            tg.MainButton.hide();
            
            console.log('Telegram Web App инициализирован');
        }
    }

    async loadData() {
        try {
            // Загружаем данные тренера
            this.data.trainer = await this.fetchTrainerData();
            
            // Загружаем клиентов
            this.data.clients = await this.fetchClientsData();
            
            // Загружаем тренировки
            this.data.workouts = await this.fetchWorkoutsData();
            
            // Обновляем UI
            this.updateTrainerInfo();
            this.updateStats();
            
        } catch (error) {
            console.error('Ошибка загрузки данных:', error);
            this.showNotification('Ошибка загрузки данных', 'error');
        }
    }

    async fetchTrainerData() {
        // Заглушка - в реальности здесь будет API запрос
        return {
            id: 1,
            name: 'Иван Иванов',
            role: 'Персональный тренер',
            email: 'ivan@example.com',
            phone: '+7 (999) 123-45-67',
            avatar: 'assets/avatar-placeholder.jpg',
            hourlyRate: 2500,
            experience: 5,
            certification: 'ACSM, NASM'
        };
    }

    async fetchClientsData() {
        // Заглушка - демо данные клиентов
        return [
            {
                id: 1,
                name: 'Анна Иванова',
                email: 'anna@example.com',
                phone: '+7 (999) 111-11-11',
                goal: 'Похудение',
                progress: 75,
                nextWorkout: '2024-06-15 10:00',
                isActive: true,
                avatar: 'АИ'
            },
            {
                id: 2,
                name: 'Петр Сидоров',
                email: 'petr@example.com',
                phone: '+7 (999) 222-22-22',
                goal: 'Набор массы',
                progress: 60,
                nextWorkout: '2024-06-15 14:00',
                isActive: true,
                avatar: 'ПС'
            },
            {
                id: 3,
                name: 'Мария Петрова',
                email: 'maria@example.com',
                phone: '+7 (999) 333-33-33',
                goal: 'Поддержание формы',
                progress: 85,
                nextWorkout: '2024-06-16 09:00',
                isActive: true,
                avatar: 'МП'
            }
        ];
    }

    async fetchWorkoutsData() {
        // Заглушка - демо данные тренировок
        return [
            {
                id: 1,
                clientId: 1,
                clientName: 'Анна Иванова',
                date: '2024-06-15',
                time: '10:00',
                duration: 60,
                type: 'Силовая',
                status: 'scheduled'
            },
            {
                id: 2,
                clientId: 2,
                clientName: 'Петр Сидоров',
                date: '2024-06-15',
                time: '14:00',
                duration: 90,
                type: 'Кардио',
                status: 'scheduled'
            }
        ];
    }

    initComponents() {
        // Инициализация компонентов
        this.sidebar = document.getElementById('sidebar');
        this.menuToggle = document.getElementById('menu-toggle');
        this.pages = document.querySelectorAll('.page');
        this.navLinks = document.querySelectorAll('.nav-link');
    }

    bindEvents() {
        // Навигация
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = link.getAttribute('data-page');
                this.navigateTo(page);
            });
        });

        // Мобильное меню
        this.menuToggle?.addEventListener('click', () => {
            this.toggleSidebar();
        });

        // Быстрые действия
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const page = btn.getAttribute('data-page');
                const action = btn.getAttribute('data-action');
                this.handleQuickAction(page, action);
            });
        });

        // Модальные окна
        document.addEventListener('click', (e) => {
            if (e.target.matches('.modal-overlay')) {
                this.closeModal();
            }
            if (e.target.matches('.modal-close')) {
                this.closeModal();
            }
        });

        // Поиск клиентов
        const clientsSearch = document.getElementById('clients-search');
        if (clientsSearch) {
            clientsSearch.addEventListener('input', (e) => {
                this.filterClients(e.target.value);
            });
        }

        // Фильтры клиентов
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.filterClients('', btn.getAttribute('data-filter'));
            });
        });

        // Уведомления
        document.getElementById('notifications-btn')?.addEventListener('click', () => {
            this.showNotifications();
        });

        // Профиль
        document.getElementById('profile-btn')?.addEventListener('click', () => {
            this.navigateTo('settings');
        });

        // Telegram бот
        document.getElementById('telegram-bot-btn')?.addEventListener('click', () => {
            this.openTelegramBot();
        });

        // Формы
        document.getElementById('profile-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveProfile();
        });

        document.getElementById('rates-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveRates();
        });
    }

    navigateTo(page) {
        // Скрываем все страницы
        this.pages.forEach(p => p.classList.remove('active'));
        
        // Показываем нужную страницу
        const targetPage = document.getElementById(`${page}-page`);
        if (targetPage) {
            targetPage.classList.add('active');
            this.currentPage = page;
        }

        // Обновляем активную ссылку в навигации
        this.navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('data-page') === page) {
                link.classList.add('active');
            }
        });

        // Загружаем данные для страницы
        this.loadPageData(page);

        // Закрываем мобильное меню
        if (window.innerWidth <= 1024) {
            this.sidebar?.classList.remove('show');
        }
    }

    async loadPageData(page) {
        switch (page) {
            case 'clients':
                this.renderClients();
                break;
            case 'workouts':
                this.renderWorkouts();
                break;
            case 'programs':
                this.renderPrograms();
                break;
            case 'analytics':
                this.initAnalyticsCharts();
                break;
            case 'dashboard':
                this.renderDashboard();
                break;
        }
    }

    toggleSidebar() {
        this.sidebar?.classList.toggle('show');
    }

    showLoader() {
        document.getElementById('loader').style.display = 'flex';
        document.getElementById('app').style.display = 'none';
    }

    hideLoader() {
        setTimeout(() => {
            document.getElementById('loader').style.display = 'none';
            document.getElementById('app').style.display = 'flex';
        }, 1500);
    }

    updateTrainerInfo() {
        const trainer = this.data.trainer;
        if (trainer) {
            document.getElementById('trainer-name').textContent = trainer.name;
            document.getElementById('trainer-role').textContent = trainer.role;
        }
    }

    updateStats() {
        // Обновляем статистику на главной
        document.getElementById('total-clients').textContent = this.data.clients.length;
        document.getElementById('total-workouts').textContent = '156';
        document.getElementById('total-revenue').textContent = '127,500₽';
        document.getElementById('today-workouts').textContent = this.data.workouts.filter(w => w.date === new Date().toISOString().split('T')[0]).length;
    }

    renderClients() {
        const clientsGrid = document.getElementById('clients-grid');
        if (!clientsGrid) return;

        clientsGrid.innerHTML = this.data.clients.map(client => `
            <div class="client-card animate-fade-in" data-client-id="${client.id}">
                <div class="client-header">
                    <div class="client-avatar">${client.avatar}</div>
                    <div class="client-info">
                        <h3>${client.name}</h3>
                        <p>${client.goal}</p>
                    </div>
                </div>
                <div class="client-stats">
                    <div class="client-stat">
                        <strong>${client.progress}%</strong>
                        <span>Прогресс</span>
                    </div>
                    <div class="client-stat">
                        <strong>${client.isActive ? 'Активен' : 'Неактивен'}</strong>
                        <span>Статус</span>
                    </div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${client.progress}%"></div>
                </div>
                <div class="client-actions">
                    <button class="btn btn-primary btn-sm" onclick="app.viewClient(${client.id})">
                        <i class="fas fa-eye"></i> Просмотр
                    </button>
                    <button class="btn btn-success btn-sm" onclick="app.scheduleWorkout(${client.id})">
                        <i class="fas fa-calendar-plus"></i> Тренировка
                    </button>
                    <button class="btn btn-secondary btn-sm" onclick="app.editClient(${client.id})">
                        <i class="fas fa-edit"></i> Изменить
                    </button>
                </div>
            </div>
        `).join('');
    }

    renderWorkouts() {
        // Рендер календаря тренировок
        const calendar = document.getElementById('workouts-calendar');
        if (!calendar) return;

        calendar.innerHTML = `
            <div class="calendar">
                <div class="calendar-header">
                    <button class="calendar-nav" onclick="app.prevMonth()">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <h3>Июнь 2024</h3>
                    <button class="calendar-nav" onclick="app.nextMonth()">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
                <div class="calendar-grid">
                    ${this.generateCalendarDays()}
                </div>
            </div>
        `;
    }

    generateCalendarDays() {
        const days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
        let html = '';

        // Заголовки дней недели
        days.forEach(day => {
            html += `<div class="calendar-day header">${day}</div>`;
        });

        // Дни месяца (заглушка)
        for (let i = 1; i <= 30; i++) {
            const hasEvents = [15, 16, 18, 22, 25].includes(i);
            const isToday = i === 15;
            html += `
                <div class="calendar-day ${isToday ? 'today' : ''} ${hasEvents ? 'has-events' : ''}" 
                     onclick="app.viewDayWorkouts(${i})">
                    ${i}
                </div>
            `;
        }

        return html;
    }

    renderPrograms() {
        const programsGrid = document.getElementById('programs-grid');
        if (!programsGrid) return;

        const programs = [
            { id: 1, name: 'Базовая силовая', exercises: 8, duration: 60 },
            { id: 2, name: 'Кардио интенсив', exercises: 6, duration: 45 },
            { id: 3, name: 'Функциональная', exercises: 10, duration: 50 }
        ];

        programsGrid.innerHTML = programs.map(program => `
            <div class="client-card">
                <div class="client-header">
                    <div class="client-avatar">
                        <i class="fas fa-clipboard-list"></i>
                    </div>
                    <div class="client-info">
                        <h3>${program.name}</h3>
                        <p>${program.exercises} упражнений • ${program.duration} мин</p>
                    </div>
                </div>
                <div class="client-actions">
                    <button class="btn btn-primary" onclick="app.editProgram(${program.id})">
                        <i class="fas fa-edit"></i> Редактировать
                    </button>
                    <button class="btn btn-success" onclick="app.useProgram(${program.id})">
                        <i class="fas fa-play"></i> Использовать
                    </button>
                </div>
            </div>
        `).join('');
    }

    renderDashboard() {
        // Обновляем расписание на сегодня
        const scheduleList = document.querySelector('.schedule-list');
        if (scheduleList) {
            const todayWorkouts = this.data.workouts.filter(w => w.date === new Date().toISOString().split('T')[0]);
            
            scheduleList.innerHTML = todayWorkouts.map(workout => `
                <div class="schedule-item">
                    <div class="schedule-time">${workout.time}</div>
                    <div class="schedule-info">
                        <strong>${workout.clientName}</strong>
                        <span>${workout.type} тренировка</span>
                    </div>
                    <div class="schedule-status ${workout.status}">
                        ${workout.status === 'scheduled' ? 'Ожидается' : 'Завершено'}
                    </div>
                </div>
            `).join('');
        }
    }

    filterClients(searchTerm = '', filter = 'all') {
        let filteredClients = this.data.clients;

        // Фильтрация по поиску
        if (searchTerm) {
            filteredClients = filteredClients.filter(client =>
                client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                client.email.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        // Фильтрация по статусу
        if (filter !== 'all') {
            filteredClients = filteredClients.filter(client => {
                if (filter === 'active') return client.isActive;
                if (filter === 'inactive') return !client.isActive;
                return true;
            });
        }

        // Временно обновляем данные для отображения
        const originalClients = this.data.clients;
        this.data.clients = filteredClients;
        this.renderClients();
        this.data.clients = originalClients;
    }

    handleQuickAction(page, action) {
        if (action === 'add') {
            switch (page) {
                case 'clients':
                    this.showAddClientModal();
                    break;
                case 'workouts':
                    this.showAddWorkoutModal();
                    break;
                case 'programs':
                    this.showAddProgramModal();
                    break;
                case 'nutrition':
                    this.showAddNutritionModal();
                    break;
            }
        } else {
            this.navigateTo(page);
        }
    }

    // Модальные окна
    showModal(title, content, footer = '') {
        const modal = document.getElementById('modal');
        const overlay = document.getElementById('modal-overlay');
        const modalTitle = document.getElementById('modal-title');
        const modalBody = document.getElementById('modal-body');
        const modalFooter = document.getElementById('modal-footer');

        modalTitle.textContent = title;
        modalBody.innerHTML = content;
        if (footer) modalFooter.innerHTML = footer;

        overlay.classList.add('show');
    }

    closeModal() {
        document.getElementById('modal-overlay').classList.remove('show');
    }

    showAddClientModal() {
        const content = `
            <form id="add-client-form">
                <div class="form-group">
                    <label>Имя</label>
                    <input type="text" id="client-name" required>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="client-email" required>
                </div>
                <div class="form-group">
                    <label>Телефон</label>
                    <input type="tel" id="client-phone" required>
                </div>
                <div class="form-group">
                    <label>Цель</label>
                    <select id="client-goal" required>
                        <option value="">Выберите цель</option>
                        <option value="weight-loss">Похудение</option>
                        <option value="muscle-gain">Набор массы</option>
                        <option value="maintenance">Поддержание формы</option>
                        <option value="strength">Развитие силы</option>
                    </select>
                </div>
            </form>
        `;

        const footer = `
            <button class="btn btn-secondary" onclick="app.closeModal()">Отмена</button>
            <button class="btn btn-primary" onclick="app.saveClient()">Сохранить</button>
        `;

        this.showModal('Добавить клиента', content, footer);
    }

    showNotification(message, type = 'info') {
        // Создаем уведомление
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}-circle"></i>
            <span>${message}</span>
        `;

        // Добавляем стили для уведомления
        if (!document.querySelector('.notification-container')) {
            const container = document.createElement('div');
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
        `;

        document.querySelector('.notification-container').appendChild(notification);

        // Автоматически удаляем через 5 секунд
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    // API методы (заглушки)
    async saveClient() {
        try {
            // Получаем данные формы
            const name = document.getElementById('client-name').value;
            const email = document.getElementById('client-email').value;
            const phone = document.getElementById('client-phone').value;
            const goal = document.getElementById('client-goal').value;

            // Создаем нового клиента
            const newClient = {
                id: this.data.clients.length + 1,
                name,
                email,
                phone,
                goal,
                progress: 0,
                isActive: true,
                avatar: name.split(' ').map(n => n[0]).join('').toUpperCase()
            };

            this.data.clients.push(newClient);
            this.renderClients();
            this.updateStats();
            this.closeModal();
            this.showNotification('Клиент успешно добавлен', 'success');

        } catch (error) {
            console.error('Ошибка сохранения клиента:', error);
            this.showNotification('Ошибка сохранения клиента', 'error');
        }
    }

    async saveProfile() {
        this.showNotification('Профиль сохранен', 'success');
    }

    async saveRates() {
        this.showNotification('Тарифы обновлены', 'success');
    }

    viewClient(clientId) {
        const client = this.data.clients.find(c => c.id === clientId);
        if (client) {
            const content = `
                <div class="client-details">
                    <div class="client-avatar large">${client.avatar}</div>
                    <h3>${client.name}</h3>
                    <p><strong>Email:</strong> ${client.email}</p>
                    <p><strong>Телефон:</strong> ${client.phone}</p>
                    <p><strong>Цель:</strong> ${client.goal}</p>
                    <p><strong>Прогресс:</strong> ${client.progress}%</p>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${client.progress}%"></div>
                    </div>
                </div>
            `;
            this.showModal(`Клиент: ${client.name}`, content);
        }
    }

    scheduleWorkout(clientId) {
        this.showNotification('Функция планирования тренировки в разработке', 'info');
    }

    editClient(clientId) {
        this.showNotification('Функция редактирования клиента в разработке', 'info');
    }

    openTelegramBot() {
        if (window.Telegram?.WebApp) {
            window.Telegram.WebApp.close();
        } else {
            this.showNotification('Откройте через Telegram', 'info');
        }
    }

    initCharts() {
        // Инициализация графика прогресса на главной
        const ctx = document.getElementById('progressChart');
        if (ctx && window.Chart) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
                    datasets: [{
                        label: 'Средний прогресс клиентов',
                        data: [45, 52, 58, 65, 70, 75],
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0, 123, 255, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        }
                    }
                }
            });
        }
    }

    initAnalyticsCharts() {
        // Инициализация графиков аналитики
        setTimeout(() => {
            this.createClientChart();
            this.createRevenueChart();
            this.createExerciseChart();
            this.createEffectivenessChart();
        }, 100);
    }

    createClientChart() {
        const ctx = document.getElementById('clientsChart');
        if (ctx && window.Chart) {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
                    datasets: [{
                        label: 'Новые клиенты',
                        data: [3, 5, 2, 8, 4, 6],
                        backgroundColor: '#007bff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }

    createRevenueChart() {
        const ctx = document.getElementById('revenueChart');
        if (ctx && window.Chart) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
                    datasets: [{
                        label: 'Доходы (₽)',
                        data: [85000, 92000, 78000, 105000, 118000, 127500],
                        borderColor: '#28a745',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }

    createExerciseChart() {
        const ctx = document.getElementById('exercisesChart');
        if (ctx && window.Chart) {
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Приседания', 'Отжимания', 'Планка', 'Жим лежа', 'Другие'],
                    datasets: [{
                        data: [25, 20, 15, 18, 22],
                        backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }

    createEffectivenessChart() {
        const ctx = document.getElementById('effectivenessChart');
        if (ctx && window.Chart) {
            new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['Сила', 'Выносливость', 'Гибкость', 'Мотивация', 'Техника'],
                    datasets: [{
                        label: 'Средние показатели',
                        data: [80, 75, 60, 85, 90],
                        borderColor: '#17a2b8',
                        backgroundColor: 'rgba(23, 162, 184, 0.2)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }
    }
}

// Инициализация приложения
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new FitnessApp();
});

// Стили для уведомлений
const notificationStyles = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;

// Добавляем стили в документ
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);
