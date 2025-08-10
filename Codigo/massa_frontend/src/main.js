import './assets/main.css';
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css'; // Importa a biblioteca de ícones do Material Design

import App from './App.vue';
import router from './router';

import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { useAuthStore } from './stores/auth';

// Cria a instância do Vuetify
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi', // Define 'mdi' como o conjunto de ícones padrão
  },
});

// Cria a aplicação
const pinia = createPinia();
const app = createApp(App);

// Usa o Vuetify, Pinia e o router
app.use(router);
app.use(vuetify);
app.use(pinia);

// Monta a aplicação
app.mount('#app');
