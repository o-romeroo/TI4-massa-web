import { defineStore } from 'pinia'
import { getAllUsersIpInfos } from '@/services/Geolocation'

export const useGeolocationStore = defineStore('geolocation', {
    state: () => ({
        infos: null,
        error: null,
    }),
    actions: {
        async fetchUsersIpInfos() {
        try {
            this.infos = await getAllUsersIpInfos()
            return this.infos
        } catch (error) {
            console.error('Error trying to fetch users IP infos: ', error)
            this.error = error
        }
        },
    },
    getters: {
        getInfos: (state) => state.infos,
    },
});