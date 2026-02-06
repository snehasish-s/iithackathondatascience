/**
 * Main Application Logic
 * Handles UI interactions, data loading, and display
 */

class CausalChatApp {
    constructor() {
        this.currentTab = 'overview';
        this.init();
    }

    /**
     * Initialize the application
     */
    init() {
        this.setupEventListeners();
        this.loadData();
        this.updateTime();
        setInterval(() => this.updateTime(), 60000);
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.closest('.tab-btn')));
        });
    }

    /**
     * Switch to a different tab
     */
    switchTab(btn) {
        const tabName = btn.dataset.tab;
        
        // Update active button
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update active content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');

        this.currentTab = tabName;
    }

    /**
     * Show loading indicator
     */
    showLoading() {
        const indicator = document.getElementById('loadingIndicator');
        if (indicator) {
            indicator.classList.add('active');
        }
    }

    /**
     * Hide loading indicator
     */
    hideLoading() {
        const indicator = document.getElementById('loadingIndicator');
        if (indicator) {
            indicator.classList.remove('active');
        }
    }

    /**
     * Load all data from API
     */
    async loadData() {
        this.showLoading();
        try {
            // Load all data in parallel
            const [stats, causes, signals, warnings, domains, intents] = await Promise.all([
                API.getStats(),
                API.getCauses(),
                API.getSignals(),
                API.getWarnings(),
                API.getDomains(),
                API.getIntents()
            ]);

            // Update UI with data
            this.updateOverview(stats, domains, intents);
            this.updateCauses(causes);
            this.updateSignals(signals);
            this.updateWarnings(warnings);

        } catch (error) {
            console.error('Error loading data:', error);
            this.showError('Failed to load data. Please check if the API is running.');
        } finally {
            this.hideLoading();
        }
    }

    /**
     * Update overview tab
     */
    updateOverview(stats, domains, intents) {
        // Update metrics
        this.setText('totalTranscripts', stats.total_transcripts.toLocaleString());
        this.setText('totalTurns', stats.total_turns.toLocaleString());
        this.setText('escalationRate', stats.escalation_rate + '%');
        this.setText('escalatedCount', stats.escalated_conversations.toLocaleString());

        // Update charts
        Charts.initEscalationChart(
            stats.escalated_conversations,
            stats.resolved_conversations
        );
        Charts.initDomainsChart(domains.domains);
        Charts.initIntentsChart(intents.intents);
    }

    /**
     * Update causes tab
     */
    updateCauses(causesData) {
        // Extract cause counts
        let causes = {};
        if (causesData.top_causes && typeof causesData.top_causes === 'object') {
            causes = causesData.top_causes;
        }

        // Map causes to display names
        const causeNames = {
            'customer_frustration': 'Customer Frustration',
            'agent_delay': 'Agent Delay',
            'agent_denial': 'Agent Denial'
        };

        const causeIds = {
            'customer_frustration': { count: 'frustrationCount', bar: 'frustrationBar', percent: 'frustrationPercent' },
            'agent_delay': { count: 'delayCount', bar: 'delayBar', percent: 'delayPercent' },
            'agent_denial': { count: 'denialCount', bar: 'denialBar', percent: 'denialPercent' }
        };

        // Calculate total
        const total = Object.values(causes).reduce((sum, val) => {
            return sum + (Array.isArray(val) ? val.length : (val || 0));
        }, 0);

        // Update each cause
        for (const [key, ids] of Object.entries(causeIds)) {
            const count = Array.isArray(causes[key]) ? causes[key].length : (causes[key] || 0);
            const percent = total > 0 ? ((count / total) * 100).toFixed(1) : 0;

            this.setText(ids.count, count);
            this.setText(ids.percent, percent + '%');
            this.updateProgressBar(ids.bar, percent);
        }

        // Update chart
        Charts.initCausesChart(causes);

        // Update evidence
        this.updateEvidence(causesData.evidence);
    }

    /**
     * Update evidence section
     */
    updateEvidence(evidence) {
        const evidenceList = document.getElementById('evidenceList');
        if (!evidenceList) return;

        evidenceList.innerHTML = '';

        if (!evidence || Object.keys(evidence).length === 0) {
            evidenceList.innerHTML = '<p class="no-data">No evidence available</p>';
            return;
        }

        for (const [cause, examples] of Object.entries(evidence)) {
            if (Array.isArray(examples)) {
                examples.forEach((example, idx) => {
                    const item = document.createElement('div');
                    item.className = 'evidence-item';
                    item.innerHTML = `
                        <strong>${cause}</strong>
                        <em>"${example}"</em>
                    `;
                    evidenceList.appendChild(item);
                });
            }
        }
    }

    /**
     * Update signals tab
     */
    updateSignals(signalsData) {
        // Update summary
        this.setText('totalSignals', signalsData.total_signals);

        // Count keywords
        let keywordCount = 0;
        if (signalsData.keywords && typeof signalsData.keywords === 'object') {
            for (const signals of Object.values(signalsData.keywords)) {
                if (signals && signals.keywords) {
                    keywordCount += signals.keywords.length;
                }
            }
        }
        this.setText('keywordCount', keywordCount);

        // Update chart
        Charts.initSignalsChart(signalsData.by_type);

        // Update keywords grid
        this.updateKeywords(signalsData.keywords);
    }

    /**
     * Update keywords grid
     */
    updateKeywords(keywords) {
        const grid = document.getElementById('keywordsGrid');
        if (!grid) return;

        grid.innerHTML = '';

        if (!keywords || Object.keys(keywords).length === 0) {
            grid.innerHTML = '<p class="no-data">No keywords available</p>';
            return;
        }

        for (const [type, config] of Object.entries(keywords)) {
            if (config && config.keywords) {
                const typeTitle = document.createElement('div');
                typeTitle.style.gridColumn = '1 / -1';
                typeTitle.innerHTML = `<h4 style="margin-bottom: 0.5rem; color: #6b7280;">${type}</h4>`;
                grid.appendChild(typeTitle);

                config.keywords.forEach(keyword => {
                    const badge = document.createElement('div');
                    badge.className = 'keyword-badge';
                    badge.textContent = keyword;
                    grid.appendChild(badge);
                });
            }
        }
    }

    /**
     * Update warnings tab
     */
    updateWarnings(warningsData) {
        // Update cards
        this.setText('highRiskCount', warningsData.high_risk_conversations);
        this.setText('multiWarningCount', warningsData.multi_signal_warnings);
        this.setText('singleWarningCount', warningsData.single_signal_warnings);

        // Update chart
        Charts.initWarningsChart(warningsData);

        // Update thresholds
        this.updateThresholds(warningsData.thresholds);
    }

    /**
     * Update thresholds list
     */
    updateThresholds(thresholds) {
        const list = document.getElementById('thresholdsList');
        if (!list) return;

        list.innerHTML = '';

        if (!thresholds || Object.keys(thresholds).length === 0) {
            list.innerHTML = '<p class="no-data">No thresholds configured</p>';
            return;
        }

        for (const [key, value] of Object.entries(thresholds)) {
            const item = document.createElement('div');
            item.className = 'threshold-item';
            item.innerHTML = `
                <span class="threshold-name">${this.formatThresholdName(key)}</span>
                <span class="threshold-value">${value}</span>
            `;
            list.appendChild(item);
        }
    }

    /**
     * Format threshold name for display
     */
    formatThresholdName(name) {
        return name
            .replace(/_/g, ' ')
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    /**
     * Update progress bar
     */
    updateProgressBar(elementId, percent) {
        const bar = document.getElementById(elementId);
        if (!bar) return;

        const afterElement = bar.querySelector('::after');
        bar.style.setProperty('--width', percent + '%');
    }

    /**
     * Set text content of element
     */
    setText(elementId, text) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = text;
        }
    }

    /**
     * Show error message
     */
    showError(message) {
        const content = document.querySelector('.content');
        if (content) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.innerHTML = `<strong>Error:</strong> ${message}`;
            content.insertBefore(errorDiv, content.firstChild);
        }
    }

    /**
     * Update footer timestamp
     */
    updateTime() {
        const element = document.getElementById('lastUpdated');
        if (element) {
            const now = new Date();
            element.textContent = now.toLocaleTimeString();
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new CausalChatApp();
});
