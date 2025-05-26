// Интеграция с Telegram Web App
class TelegramIntegration {
    constructor() {
        this.tg = window.Telegram?.WebApp;
        this.isInTelegram = !!this.tg;
        this.user = null;
        
        if (this.isInTelegram) {
            this.init();
        }
    }

    init() {
        // Настраиваем Web App
        this.tg.expand();
        this.tg.ready();
        
        // Получаем данные пользователя
        this.user = this.tg.initDataUnsafe?.user;
        
        // Настраиваем тему
        this.setupTheme();
        
        // Настраиваем кнопки
        this.setupButtons();
        
        // Обработчики событий
        this.setupEventHandlers();
        
        console.log('Telegram Web App инициализирован', {
            user: this.user,
            platform: this.tg.platform,
            version: this.tg.version
        });
    }

    setupTheme() {
        const params = this.tg.themeParams;
        
        if (params) {
            // Применяем цвета темы Telegram
            document.documentElement.style.setProperty(
                '--primary-color', 
                params.button_color || '#007bff'
            );
            document.documentElement.style.setProperty(
                '--bg-color', 
                params.bg_color || '#ffffff'
            );
            document.documentElement.style.setProperty(
                '--text-color', 
                params.text_color || '#212529'
            );
            document.documentElement.style.setProperty(
                '--secondary-color', 
                params.hint_color || '#6c757d'
            );
            document.documentElement.style.setProperty(
                '--surface-color', 
                params.secondary_bg_color || '#f8f9fa'
            );
        }

        // Определяем тему (светлая/темная)
        if (params?.bg_color) {
            const rgb = this.hexToRgb(params.bg_color);
            const brightness = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
            
            if (brightness < 128) {
                document.documentElement.setAttribute('data-theme', 'dark');
            }
        }
    }

    setupButtons() {
        // Главная кнопка
        this.tg.MainButton.setText('Сохранить');
        this.tg.MainButton.hide();
        
        // Кнопка назад
        this.tg.BackButton.hide();
    }

    setupEventHandlers() {
        // Главная кнопка
        this.tg.onEvent('mainButtonClicked', () => {
            this.handleMainButtonClick();
        });

        // Кнопка назад
        this.tg.onEvent('backButtonClicked', () => {
            this.handleBackButtonClick();
        });

        // Закрытие приложения
        this.tg.onEvent('viewportChanged', () => {
            console.log('Viewport изменен:', this.tg.viewportHeight);
        });

        // Изменение темы
        this.tg.onEvent('themeChanged', () => {
            this.setupTheme();
        });
    }

    // Управление кнопками
    showMainButton(text = 'Сохранить', callback = null) {
        this.tg.MainButton.setText(text);
        this.tg.MainButton.show();
        
        if (callback) {
            this.mainButtonCallback = callback;
        }
    }

    hideMainButton() {
        this.tg.MainButton.hide();
        this.mainButtonCallback = null;
    }

    showBackButton() {
        this.tg.BackButton.show();
    }

    hideBackButton() {
        this.tg.BackButton.hide();
    }

    // Обработчики событий кнопок
    handleMainButtonClick() {
        if (this.mainButtonCallback) {
            this.mainButtonCallback();
        } else {
            // Действие по умолчанию
            this.saveCurrentForm();
        }
    }

    handleBackButtonClick() {
        // Возврат к предыдущей странице или закрытие модального окна
        if (document.querySelector('.modal-overlay.show')) {
            document.querySelector('.modal-overlay').classList.remove('show');
        } else if (window.app?.currentPage !== 'dashboard') {
            window.app?.navigateTo('dashboard');
        } else {
            this.closeApp();
        }
    }

    // Отправка данных в бот
    sendDataToBot(data) {
        if (this.isInTelegram) {
            this.tg.sendData(JSON.stringify(data));
        }
    }

    // Закрытие приложения
    closeApp() {
        if (this.isInTelegram) {
            this.tg.close();
        }
    }

    // Показать всплывающее уведомление
    showAlert(message) {
        if (this.isInTelegram) {
            this.tg.showAlert(message);
        } else {
            alert(message);
        }
    }

    // Показать подтверждение
    showConfirm(message, callback) {
        if (this.isInTelegram) {
            this.tg.showConfirm(message, callback);
        } else {
            const result = confirm(message);
            callback(result);
        }
    }

    // Показать popup
    showPopup(params) {
        if (this.isInTelegram && this.tg.showPopup) {
            this.tg.showPopup(params);
        }
    }

    // Включить/выключить вибрацию
    hapticFeedback(type = 'impact', style = 'medium') {
        if (this.isInTelegram && this.tg.HapticFeedback) {
            if (type === 'impact') {
                this.tg.HapticFeedback.impactOccurred(style);
            } else if (type === 'notification') {
                this.tg.HapticFeedback.notificationOccurred(style);
            } else if (type === 'selection') {
                this.tg.HapticFeedback.selectionChanged();
            }
        }
    }

    // Открыть ссылку
    openLink(url, options = {}) {
        if (this.isInTelegram) {
            this.tg.openLink(url, options);
        } else {
            window.open(url, '_blank');
        }
    }

    // Открыть Telegram ссылку
    openTelegramLink(url) {
        if (this.isInTelegram) {
            this.tg.openTelegramLink(url);
        }
    }

    // Поделиться
    shareUrl(url, text = '') {
        const shareUrl = `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`;
        this.openTelegramLink(shareUrl);
    }

    // Сканировать QR код
    showScanQrPopup(text, callback) {
        if (this.isInTelegram && this.tg.showScanQrPopup) {
            this.tg.showScanQrPopup({
                text: text
            }, callback);
        }
    }

    // Запросить контакт
    requestContact(callback) {
        if (this.isInTelegram && this.tg.requestContact) {
            this.tg.requestContact(callback);
        }
    }

    // Работа с облачным хранилищем
    getCloudStorage() {
        return this.tg?.CloudStorage;
    }

    saveToCloud(key, value) {
        const storage = this.getCloudStorage();
        if (storage) {
            storage.setItem(key, value);
        }
    }

    getFromCloud(key, callback) {
        const storage = this.getCloudStorage();
        if (storage) {
            storage.getItem(key, callback);
        }
    }

    // Получить данные пользователя
    getUserData() {
        return {
            id: this.user?.id,
            firstName: this.user?.first_name,
            lastName: this.user?.last_name,
            username: this.user?.username,
            languageCode: this.user?.language_code,
            isPremium: this.user?.is_premium
        };
    }

    // Проверка возможностей
    canUseFeature(feature) {
        const features = {
            'mainButton': !!this.tg?.MainButton,
            'backButton': !!this.tg?.BackButton,
            'hapticFeedback': !!this.tg?.HapticFeedback,
            'cloudStorage': !!this.tg?.CloudStorage,
            'scanQr': !!this.tg?.showScanQrPopup,
            'requestContact': !!this.tg?.requestContact,
            'showPopup': !!this.tg?.showPopup
        };
        
        return features[feature] || false;
    }

    // Сохранение текущей формы
    saveCurrentForm() {
        const activeModal = document.querySelector('.modal-overlay.show');
        if (activeModal) {
            const form = activeModal.querySelector('form');
            if (form) {
                // Эмулируем отправку формы
                const event = new Event('submit', { bubbles: true, cancelable: true });
                form.dispatchEvent(event);
            }
        }
    }

    // Утилиты
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }

    // Отправка аналитики
    sendAnalytics(event, params = {}) {
        const data = {
            event,
            params: {
                ...params,
                user_id: this.user?.id,
                timestamp: Date.now(),
                platform: this.tg?.platform || 'web'
            }
        };

        // Отправляем в бот для логирования
        this.sendDataToBot({
            type: 'analytics',
            data
        });
    }

    // Интеграция с приложением
    setupAppIntegration() {
        // Слушаем события приложения
        document.addEventListener('clientAdded', (e) => {
            this.hapticFeedback('notification', 'success');
            this.sendAnalytics('client_added', e.detail);
        });

        document.addEventListener('workoutScheduled', (e) => {
            this.hapticFeedback('impact', 'light');
            this.sendAnalytics('workout_scheduled', e.detail);
        });

        document.addEventListener('pageChanged', (e) => {
            this.sendAnalytics('page_view', { page: e.detail.page });
        });

        // Показываем кнопку "Назад" на внутренних страницах
        document.addEventListener('pageChanged', (e) => {
            if (e.detail.page !== 'dashboard') {
                this.showBackButton();
            } else {
                this.hideBackButton();
            }
        });

        // Показываем главную кнопку при открытии форм
        document.addEventListener('modalOpened', (e) => {
            if (e.detail.type === 'form') {
                this.showMainButton('Сохранить');
            }
        });

        document.addEventListener('modalClosed', () => {
            this.hideMainButton();
        });
    }
}

// Создаем глобальный экземпляр
window.telegramIntegration = new TelegramIntegration();

// Инициализируем интеграцию с приложением после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    if (window.telegramIntegration.isInTelegram) {
        window.telegramIntegration.setupAppIntegration();
    }
});
