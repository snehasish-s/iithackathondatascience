/**
 * Chart.js Chart Initialization and Management
 */

const Charts = {
    instances: {},

    /**
     * Create or update escalation chart
     */
    initEscalationChart(escalated, resolved) {
        const ctx = document.getElementById('escalationChart');
        if (!ctx) return;

        if (this.instances.escalation) {
            this.instances.escalation.destroy();
        }

        this.instances.escalation = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Escalated', 'Resolved'],
                datasets: [{
                    data: [escalated, resolved],
                    backgroundColor: ['#dc2626', '#16a34a'],
                    borderColor: ['#991b1b', '#15803d'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    },

    /**
     * Create or update domains chart
     */
    initDomainsChart(domainData) {
        const ctx = document.getElementById('domainsChart');
        if (!ctx) return;

        const labels = Object.keys(domainData).slice(0, 6);
        const data = Object.values(domainData).slice(0, 6);

        if (this.instances.domains) {
            this.instances.domains.destroy();
        }

        this.instances.domains = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Conversations',
                    data: data,
                    backgroundColor: '#2563eb',
                    borderColor: '#1e40af',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    },

    /**
     * Create or update intents chart
     */
    initIntentsChart(intentData) {
        const ctx = document.getElementById('intentsChart');
        if (!ctx) return;

        const labels = Object.keys(intentData);
        const data = Object.values(intentData);

        if (this.instances.intents) {
            this.instances.intents.destroy();
        }

        this.instances.intents = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Count',
                    data: data,
                    backgroundColor: [
                        '#2563eb', '#0ea5e9', '#10b981',
                        '#f59e0b', '#dc2626', '#8b5cf6'
                    ],
                    borderRadius: 4,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'x',
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    },
                    x: {
                        ticks: {
                            font: {
                                size: 11
                            }
                        }
                    }
                }
            }
        });
    },

    /**
     * Create or update causes chart
     */
    initCausesChart(causesData) {
        const ctx = document.getElementById('causesChart');
        if (!ctx) return;

        const labels = Object.keys(causesData);
        const data = Object.values(causesData).map(item => 
            Array.isArray(item) ? item.length : item
        );

        if (this.instances.causes) {
            this.instances.causes.destroy();
        }

        this.instances.causes = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#dc2626',
                        '#f59e0b',
                        '#6366f1'
                    ],
                    borderColor: [
                        '#991b1b',
                        '#d97706',
                        '#4f46e5'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    },

    /**
     * Create or update signals chart
     */
    initSignalsChart(signalsData) {
        const ctx = document.getElementById('signalsChart');
        if (!ctx) return;

        const labels = Object.keys(signalsData);
        const data = Object.values(signalsData);

        if (this.instances.signals) {
            this.instances.signals.destroy();
        }

        this.instances.signals = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#dc2626',
                        '#f59e0b',
                        '#6366f1'
                    ],
                    borderColor: [
                        '#991b1b',
                        '#d97706',
                        '#4f46e5'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    },

    /**
     * Create or update warnings chart
     */
    initWarningsChart(warningData) {
        const ctx = document.getElementById('warningsChart');
        if (!ctx) return;

        if (this.instances.warnings) {
            this.instances.warnings.destroy();
        }

        this.instances.warnings = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Single-Signal', 'Multi-Signal', 'High Risk'],
                datasets: [{
                    label: 'Count',
                    data: [
                        warningData.single_signal_warnings || 0,
                        warningData.multi_signal_warnings || 0,
                        warningData.high_risk_conversations || 0
                    ],
                    backgroundColor: ['#0ea5e9', '#f59e0b', '#dc2626'],
                    borderWidth: 0,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    },

    /**
     * Destroy all charts
     */
    destroyAll() {
        Object.values(this.instances).forEach(chart => {
            if (chart) {
                chart.destroy();
            }
        });
        this.instances = {};
    }
};
