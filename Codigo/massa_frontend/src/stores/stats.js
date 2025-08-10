import { defineStore } from 'pinia';
import StatsService from '@/services/StatsService';
import { ref } from 'vue';

function isRecentTimestamp(timestamp, minutesAgo) {
    if(timestamp == null) {
        return false;
    }

    const now = Date.now();
    const timestampMillis = new Date(timestamp).getTime();
    const minutesAgoMillis = minutesAgo * 60 * 1000;
    return now - timestampMillis <= minutesAgoMillis;
}

export const useStatsStore = defineStore('stats', {
    state: () => ({
        stats: null,
        last_fetch: null
    }),
    actions: {
        async fetchStats() {         

            this.last_fetch = sessionStorage.getItem('stats_last_fetch');

            if(!isRecentTimestamp(this.last_fetch)) {
                try {
                    this.stats = await StatsService.getStats();
                    this.last_fetch = Date.now();
                    sessionStorage.setItem('stats_last_fetch', this.last_fetch);
                    
                    return this.stats;
                } catch (error) {
                    console.error('Error trying to fetch stats: ', error);
                }
            }
        },
    },
    getters: {
        getStats: (state) => state.stats,
    },
});