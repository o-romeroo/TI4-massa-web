import { defineStore } from 'pinia';
import LoginService from '@/services/LoginService';
import RegisterService from '@/services/RegisterService';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    token: localStorage.getItem('token') || null,
    username: localStorage.getItem('username') || null,
  }),
  getters: {
  },
  actions: {
    async login(username, password) {
      const cleanedUsername = username.replace(/[^a-zA-Z]/g, '');
      try {
        const token = await LoginService.login(username, password);
        this.token = token;
        localStorage.setItem('token', this.token);
        this.isAuthenticated = true;
        this.username = cleanedUsername; 
        localStorage.setItem('username', cleanedUsername); 
      } catch (error) {
        this.isAuthenticated = false;
        this.token = null;
        this.username = null;
        throw error;
      }
    },
    async register(userData) {
      const cleanedUsername = userData.username.replace(/[^a-zA-Z]/g, '');
      try {
        const token = await RegisterService.register(userData);
        this.token = token;
        localStorage.setItem('token', this.token);
        this.isAuthenticated = true;
        this.username = cleanedUsername; 
        localStorage.setItem('username', cleanedUsername); 
      } catch (error) {
        this.isAuthenticated = false;
        this. token = null;
        this.username = null;
        throw error;
      }
    },
    logout() {
      LoginService.logout();
      this.isAuthenticated = false;
      this.token = null;
      this.username = null;
      localStorage.removeItem('token');
      localStorage.removeItem('username'); 
    },
  },
});