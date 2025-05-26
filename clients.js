// Модуль управления клиентами
class ClientsManager {
    constructor() {
        this.clients = [];
        this.filteredClients = [];
        this.currentFilter = 'all';
        this.searchTerm = '';
        this.sortBy = 'name';
        this.sortOrder = 'asc';
        
        this.initEventListeners();
    }

    initEventListeners() {
        // Поиск клиентов
        const searchInput = document.getElementById('clients-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchTerm = e.target.value.toLowerCase();
                this.filterAndRenderClients();
            });
        }

        // Фильтры
        document.addEventListener('click', (e) => {
            if (e.target.matches('.filter-btn')) {
                document.querySelectorAll('.filter-btn').forEach(btn => 
                    btn.classList.remove('active')
                );
                e.target.classList.add('active');
                this.currentFilter = e.target.dataset.filter;
                this.filterAndRenderClients();
            }
        });
    }

    setClients(clients) {
        this.clients = clients;
        this.filteredClients = [...clients];
        this.renderClients();
    }

    filterAndRenderClients() {
        this.filteredClients = this.clients.filter(client => {
            // Фильтр по статусу
            let statusMatch = true;
            if (this.currentFilter === 'active') {
                statusMatch = client.isActive;
            } else if (this.currentFilter === 'inactive') {
                statusMatch = !client.isActive;
            }

            // Поиск по имени, email или телефону
            let searchMatch = true;
            if (this.searchTerm) {
                searchMatch = client.name.toLowerCase().includes(this.searchTerm) ||
                             client.email.toLowerCase().includes(this.searchTerm) ||
                             (client.phone && client.phone.includes(this.searchTerm));
            }

            return statusMatch && searchMatch;
        });

        this.renderClients();
    }

    renderClients() {
        const clientsGrid = document.getElementById('clients-grid');
        if (!clientsGrid) return;

        if (this.filteredClients.length === 0) {
            clientsGrid.innerHTML = this.renderEmptyState();
            return;
        }

        clientsGrid.innerHTML = this.filteredClients.map(client => 
            this.renderClientCard(client)
        ).join('');
    }

    renderClientCard(client) {
        const nextWorkoutDate = client.nextWorkout ? 
            new Date(client.nextWorkout).toLocaleDateString('ru-RU') : 'Не запланирована';

        return `
            <div class="client-card" data-client-id="${client.id}">
                <div class="client-header">
                    <div class="client-avatar">${client.avatar}</div>
                    <div class="client-info">
                        <h3>${client.name}</h3>
                        <p>${client.goal || 'Цель не указана'}</p>
                    </div>
                </div>
                <div class="client-stats">
                    <div class="client-stat">
                        <strong>${client.progress || 0}%</strong>
                        <span>Прогресс</span>
                    </div>
                    <div class="client-stat">
                        <strong>${client.isActive ? 'Активен' : 'Неактивен'}</strong>
                        <span>Статус</span>
                    </div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${client.progress || 0}%"></div>
                </div>
                <div class="client-actions">
                    <button class="btn btn-primary btn-sm" onclick="clientsManager.viewClient(${client.id})">
                        <i class="fas fa-eye"></i> Просмотр
                    </button>
                    <button class="btn btn-success btn-sm" onclick="clientsManager.scheduleWorkout(${client.id})">
                        <i class="fas fa-calendar-plus"></i> Тренировка
                    </button>
                </div>
            </div>
        `;
    }

    renderEmptyState() {
        return `
            <div class="empty-state">
                <i class="fas fa-users fa-3x"></i>
                <h3>Клиенты не найдены</h3>
                <p>Попробуйте изменить параметры поиска</p>
            </div>
        `;
    }

    viewClient(clientId) {
        const client = this.clients.find(c => c.id === clientId);
        if (client && window.app) {
            window.app.viewClient(clientId);
        }
    }

    scheduleWorkout(clientId) {
        if (window.app) {
            window.app.scheduleWorkout(clientId);
        }
    }
}

// Создаем глобальный экземпляр
window.clientsManager = new ClientsManager();
