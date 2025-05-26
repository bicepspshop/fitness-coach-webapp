// Упрощенная версия приложения для быстрой загрузки
class SimpleFitnessApp {
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
                { id: 1, name: 'Анна Иванова', goal: 'Похудение', progress: 75 },
                { id: 2, name: 'Петр Сидоров', goal: 'Набор массы', progress: 60 },
                { id: 3, name: 'Мария Петрова', goal: 'Поддержание формы', progress: 85 }
            ]
        };
        this.init();
    }

    init() {
        console.log('Инициализация приложения...');
        this.bindEvents();
        this.updateStats();
        this.renderClients();
        this.initSimpleChart();
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
                const page = btn.getAttribute('data-page');
                this.navigateTo(page);
            });
        });

        // Уведомления
        document.getElementById('notifications-btn')?.addEventListener('click', () => {
            this.showNotification('У вас 3 новых уведомления', 'info');
        });
    }

    navigateTo(page) {
        // Скрываем все страницы
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        
        // Показываем нужную страницу
        const targetPage = document.getElementById(`${page}-page`);
        if (targetPage) {
            targetPage.classList.add('active');
            this.currentPage = page;
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
    }

    loadPageData(page) {
        switch (page) {
            case 'clients':
                this.renderClients();
                break;
            case 'analytics':
                this.initAnalyticsCharts();
                break;
        }
    }

    toggleSidebar() {
        document.getElementById('sidebar')?.classList.toggle('show');
    }

    updateStats() {
        const stats = this.data.trainer;
        document.getElementById('total-clients').textContent = stats.clients;
        document.getElementById('total-workouts').textContent = stats.workouts;
        document.getElementById('total-revenue').textContent = stats.revenue.toLocaleString() + '₽';
        document.getElementById('today-workouts').textContent = '5';
    }

    renderClients() {
        const clientsGrid = document.getElementById('clients-grid');
        if (!clientsGrid) return;

        clientsGrid.innerHTML = this.data.clients.map(client => `
            <div class="client-card">
                <div class="client-header">
                    <div class="client-avatar">${this.getInitials(client.name)}</div>
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
                        <strong>Активен</strong>
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
                    <button class="btn btn-success btn-sm">
                        <i class="fas fa-calendar-plus"></i> Тренировка
                    </button>
                </div>
            </div>
        `).join('');
    }

    getInitials(name) {
        return name.split(' ').map(n => n[0]).join('').toUpperCase();
    }

    viewClient(clientId) {
        const client = this.data.clients.find(c => c.id === clientId);
        if (client) {
            this.showNotification(`Просмотр клиента: ${client.name}`, 'info');
        }
    }

    showNotification(message, type = 'info') {
        // Создаем уведомление
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
        `;

        container.appendChild(notification);

        // Удаляем через 3 секунды
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    initSimpleChart() {
        const ctx = document.getElementById('progressChart');
        if (ctx && window.Chart) {
            try {
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
                        datasets: [{
                            label: 'Прогресс клиентов',
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
                            legend: { display: false }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });
            } catch (e) {
                console.log('Chart.js не загружен, график пропущен');
            }
        }
    }

    initAnalyticsCharts() {
        setTimeout(() => {
            this.createChart('clientsChart', 'bar', ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'], [3, 5, 2, 8, 4, 6]);
            this.createChart('revenueChart', 'line', ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'], [85000, 92000, 78000, 105000, 118000, 127500]);
        }, 100);
    }

    createChart(canvasId, type, labels, data) {
        const ctx = document.getElementById(canvasId);
        if (ctx && window.Chart) {
            try {
                new Chart(ctx, {
                    type: type,
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Данные',
                            data: data,
                            borderColor: '#007bff',
                            backgroundColor: type === 'line' ? 'rgba(0, 123, 255, 0.1)' : '#007bff',
                            fill: type === 'line'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
            } catch (e) {
                console.log(`Не удалось создать график ${canvasId}`);
            }
        }
    }
}

// Инициализация при загрузке DOM
let app;
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM загружен, инициализируем приложение...');
    
    // Небольшая задержка для загрузки всех ресурсов
    setTimeout(() => {
        app = new SimpleFitnessApp();
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
`;
document.head.appendChild(styles);
