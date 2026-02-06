/**
 * API Client for Causal Chat Analysis
 * Handles all communication with the Flask backend
 */

const API = {
    BASE_URL: 'http://localhost:5000/api',

    /**
     * Make an API request
     */
    async request(endpoint) {
        try {
            const response = await fetch(`${this.BASE_URL}${endpoint}`);
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Unknown error');
            }
            
            return data.data;
        } catch (error) {
            console.error(`Error calling ${endpoint}:`, error);
            throw error;
        }
    },

    /**
     * Get overall statistics
     */
    async getStats() {
        return this.request('/stats');
    },

    /**
     * Get causal analysis results
     */
    async getCauses() {
        return this.request('/causes');
    },

    /**
     * Get signal extraction results
     */
    async getSignals() {
        return this.request('/signals');
    },

    /**
     * Get early warning results
     */
    async getWarnings() {
        return this.request('/warnings');
    },

    /**
     * Get domain breakdown
     */
    async getDomains() {
        return this.request('/domains');
    },

    /**
     * Get intent breakdown
     */
    async getIntents() {
        return this.request('/intents');
    },

    /**
     * Get specific transcript
     */
    async getTranscript(transcriptId) {
        return this.request(`/transcript/${transcriptId}`);
    },

    /**
     * Health check
     */
    async health() {
        try {
            return await this.request('/health');
        } catch (error) {
            return null;
        }
    }
};
