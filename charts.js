// Модуль для работы с графиками
class ChartsManager {
    constructor() {
        this.charts = new Map();
        this.defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#007bff',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: false
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            }
        };
    }

    createChart(canvasId, config) {
        const canvas = document.getElementById(canvasId);
        if (!canvas || !window.Chart) {
            console.warn(`Canvas ${canvasId} not found or Chart.js not loaded`);
            return null;
        }

        // Уничтожаем существующий график
        if (this.charts.has(canvasId)) {
            this.charts.get(canvasId).destroy();
        }

        // Объединяем настройки с дефолтными
        const mergedConfig = this.mergeDeep(config, { options: this.defaultOptions });

        // Создаем новый график
        const chart = new Chart(canvas, mergedConfig);
        this.charts.set(canvasId, chart);

        return chart;
    }

    updateChart(canvasId, newData) {
        const chart = this.charts.get(canvasId);
        if (chart) {
            chart.data = newData;
            chart.update('active');
        }
    }

    destroyChart(canvasId) {
        const chart = this.charts.get(canvasId);
        if (chart) {
            chart.destroy();
            this.charts.delete(canvasId);
        }
    }

    destroyAllCharts() {
        this.charts.forEach((chart, id) => {
            chart.destroy();
        });
        this.charts.clear();
    }

    // Специфические графики для фитнес-приложения

    createProgressChart(canvasId, clientsData) {
        const data = {
            labels: this.getLastSixMonths(),
            datasets: [{
                label: 'Средний прогресс клиентов (%)',
                data: this.calculateMonthlyProgress(clientsData),
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#007bff',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        };

        return this.createChart(canvasId, {
            type: 'line',
            data: data,
            options: {
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

    createWorkoutDistributionChart(canvasId, workoutsData) {
        const workoutTypes = this.aggregateWorkoutTypes(workoutsData);
        
        const data = {
            labels: Object.keys(workoutTypes),
            datasets: [{
                data: Object.values(workoutTypes),
                backgroundColor: [
                    '#007bff',
                    '#28a745', 
                    '#ffc107',
                    '#dc3545',
                    '#6c757d',
                    '#17a2b8'
                ],
                borderWidth: 0,
                hoverBorderWidth: 3,
                hoverBorderColor: '#fff'
            }]
        };

        return this.createChart(canvasId, {
            type: 'doughnut',
            data: data,
            options: {
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    createRevenueChart(canvasId, revenueData) {
        const data = {
            labels: this.getLastSixMonths(),
            datasets: [{
                label: 'Доходы (₽)',
                data: revenueData || [85000, 92000, 78000, 105000, 118000, 127500],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                fill: true,
                tension: 0.3,
                pointBackgroundColor: '#28a745',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        };

        return this.createChart(canvasId, {
            type: 'line',
            data: data,
            options: {
                scales: {
                    y: {
                        ticks: {
                            callback: function(value) {
                                return new Intl.NumberFormat('ru-RU', {
                                    style: 'currency',
                                    currency: 'RUB',
                                    minimumFractionDigits: 0
                                }).format(value);
                            }
                        }
                    }
                }
            }
        });
    }

    createClientAcquisitionChart(canvasId, clientsData) {
        const monthlyAcquisition = this.calculateMonthlyClientAcquisition(clientsData);
        
        const data = {
            labels: this.getLastSixMonths(),
            datasets: [{
                label: 'Новые клиенты',
                data: monthlyAcquisition,
                backgroundColor: '#007bff',
                borderRadius: 6,
                borderSkipped: false,
                barThickness: 30
            }, {
                label: 'Цель',
                data: [5, 5, 5, 5, 5, 5], // Целевое количество новых клиентов
                type: 'line',
                borderColor: '#dc3545',
                backgroundColor: 'transparent',
                borderDash: [5, 5],
                pointRadius: 0,
                tension: 0
            }]
        };

        return this.createChart(canvasId, {
            type: 'bar',
            data: data,
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    createBodyMetricsChart(canvasId, clientId, metricsData) {
        // График изменения параметров тела клиента
        const data = {
            labels: metricsData.dates || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Вес (кг)',
                data: metricsData.weight || [75, 73, 71, 70, 68, 67],
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                yAxisID: 'y'
            }, {
                label: 'Процент жира (%)',
                data: metricsData.bodyFat || [22, 21, 19, 18, 17, 16],
                borderColor: '#dc3545',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                yAxisID: 'y1'
            }]
        };

        return this.createChart(canvasId, {
            type: 'line',
            data: data,
            options: {
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Вес (кг)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Процент жира (%)'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                }
            }
        });
    }

    createWorkoutIntensityChart(canvasId, workoutData) {
        // Радарная диаграмма интенсивности тренировок
        const data = {
            labels: ['Сила', 'Выносливость', 'Гибкость', 'Координация', 'Скорость', 'Мощность'],
            datasets: [{
                label: 'Текущий уровень',
                data: workoutData.current || [80, 75, 60, 70, 65, 85],
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.2)',
                pointBackgroundColor: '#007bff'
            }, {
                label: 'Целевой уровень',
                data: workoutData.target || [90, 85, 80, 80, 75, 90],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                pointBackgroundColor: '#28a745'
            }]
        };

        return this.createChart(canvasId, {
            type: 'radar',
            data: data,
            options: {
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20
                        }
                    }
                }
            }
        });
    }

    createAttendanceChart(canvasId, attendanceData) {
        // График посещаемости
        const data = {
            labels: this.getLastFourWeeks(),
            datasets: [{
                label: 'Запланировано',
                data: attendanceData.scheduled || [15, 18, 16, 20],
                backgroundColor: 'rgba(108, 117, 125, 0.6)',
                borderRadius: 4
            }, {
                label: 'Посещено',
                data: attendanceData.attended || [14, 16, 15, 18],
                backgroundColor: '#28a745',
                borderRadius: 4
            }, {
                label: 'Пропущено',
                data: attendanceData.missed || [1, 2, 1, 2],
                backgroundColor: '#dc3545',
                borderRadius: 4
            }]
        };

        return this.createChart(canvasId, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                scales: {
                    x: {
                        stacked: true,
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Утилиты для обработки данных

    getLastSixMonths() {
        const months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];
        const now = new Date();
        const result = [];
        
        for (let i = 5; i >= 0; i--) {
            const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
            result.push(months[date.getMonth()]);
        }
        
        return result;
    }

    getLastFourWeeks() {
        const result = [];
        const now = new Date();
        
        for (let i = 3; i >= 0; i--) {
            const weekStart = new Date(now.getTime() - (i * 7 * 24 * 60 * 60 * 1000));
            const weekNumber = Math.ceil(weekStart.getDate() / 7);
            result.push(`Неделя ${weekNumber}`);
        }
        
        return result;
    }

    calculateMonthlyProgress(clientsData) {
        // Заглушка - в реальном приложении здесь будет расчет на основе данных
        return [45, 52, 58, 65, 70, 75];
    }

    calculateMonthlyClientAcquisition(clientsData) {
        // Заглушка - расчет новых клиентов по месяцам
        return [3, 5, 2, 8, 4, 6];
    }

    aggregateWorkoutTypes(workoutsData) {
        // Заглушка - агрегация типов тренировок
        return {
            'Силовые': 35,
            'Кардио': 25,
            'Функциональные': 20,
            'Растяжка': 12,
            'Групповые': 8
        };
    }

    // Утилита для глубокого слияния объектов
    mergeDeep(target, source) {
        const output = Object.assign({}, target);
        if (this.isObject(target) && this.isObject(source)) {
            Object.keys(source).forEach(key => {
                if (this.isObject(source[key])) {
                    if (!(key in target))
                        Object.assign(output, { [key]: source[key] });
                    else
                        output[key] = this.mergeDeep(target[key], source[key]);
                } else {
                    Object.assign(output, { [key]: source[key] });
                }
            });
        }
        return output;
    }

    isObject(item) {
        return (item && typeof item === "object" && !Array.isArray(item));
    }

    // Экспорт данных графиков
    exportChartData(canvasId, format = 'png') {
        const chart = this.charts.get(canvasId);
        if (chart) {
            const url = chart.toBase64Image();
            const link = document.createElement('a');
            link.download = `chart-${canvasId}-${Date.now()}.${format}`;
            link.href = url;
            link.click();
        }
    }

    // Обновление цветовой схемы графиков
    updateTheme(isDark = false) {
        const textColor = isDark ? '#ffffff' : '#212529';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)';

        this.defaultOptions.plugins.legend.labels.color = textColor;
        this.defaultOptions.scales.x.ticks = { color: textColor };
        this.defaultOptions.scales.y.ticks = { color: textColor };
        this.defaultOptions.scales.x.grid.color = gridColor;
        this.defaultOptions.scales.y.grid.color = gridColor;

        // Обновляем все существующие графики
        this.charts.forEach((chart) => {
            chart.options.plugins.legend.labels.color = textColor;
            if (chart.options.scales.x) chart.options.scales.x.ticks.color = textColor;
            if (chart.options.scales.y) chart.options.scales.y.ticks.color = textColor;
            chart.update('none');
        });
    }
}

// Глобальный экземпляр менеджера графиков
window.ChartsManager = ChartsManager;
