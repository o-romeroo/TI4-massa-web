<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar>
        <div class="toolbarContent">
          <v-toolbar-title>
            <div style="align-items: center; display:flex;">
              <img src="../assets/logo_massa.svg" alt="Logo" width="max-content" />
              <div class="conjuntoTitlesMassa">
                <h1 class="titleMassa">MASSA</h1>
                <h4 class="titleMassa2">Molecular dAta Set Sampling Algorithm</h4>
              </div>
            </div>
          </v-toolbar-title>

          <v-toolbar-items class="hidden-sm-and-down">
            <v-btn variant="plain" to="/">
              <p style="color: black; font-weight: bold;">Home</p>
            </v-btn>
            <v-btn variant="plain" to="/execution">
              <p style="color: black; font-weight: bold">Execute</p>
            </v-btn>
            <v-btn variant="plain" to="/algorithm">
              <p style="color: black; font-weight: bold">Algorithm</p>
            </v-btn>
            <v-btn variant="plain" to="/about">
              <p style="color: black; font-weight: bold">About</p>
            </v-btn>
            <v-btn variant="plain" to="/support">
              <p style="color: black; font-weight: bold">Support</p>
            </v-btn>
            <v-btn variant="plain" to="/data">
              <p style="color: black; font-weight: bold">Data</p>
            </v-btn>
            <v-divider class="mx-2" vertical></v-divider>
            <v-menu v-if="isLogged" offset-y>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" variant="plain" class="d-flex align-center">
                  <v-icon class="me-2">mdi-account-circle</v-icon>
                  <span style="font-weight: bold;">{{ username }}</span>
                  <v-icon class="ms-2">mdi-menu-down</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="logout">
                  <v-list-item-title>Logout</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <v-btn v-else variant="plain" to="/login">
              <p style="color: black; font-weight: bold">Login</p>
            </v-btn>
          </v-toolbar-items>
        </div>
      </v-toolbar>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>

    <v-snackbar v-model="showAlert" :timeout="4000" top multi-line color="success">
      {{ alertMessage }}
      <template v-slot:actions="{ attrs }">
        <v-btn icon @click="showAlert = false" v-bind="attrs">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>

    <v-footer class="footer pt-10 pb-0 mb-0">
      <span> MASSA - Molecular dAta Set Sampling Algorithm © 2024</span>
    </v-footer>

  </v-app>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  name: "MainLayout",
  data() {
    return {
      showAlert: false,
      alertMessage: '',
    };
  },
  computed: {
    isLogged() {
      return useAuthStore().isAuthenticated;
    },
    username() {
      return useAuthStore().username;
    },
  },
  methods: {
    async logout() {
      const authStore = useAuthStore();
      try {
        authStore.logout();
        this.$router.push('/');
        this.alertMessage = 'Logout completed successfully!';
        this.showAlert = true;
      } catch (error) {
        console.error("Logout error:", error);
      }
    },
  },
};
</script>

<style>
.footer {
  text-align: center;
  display: flex;
  justify-content: center;
  width: 100%;
}

.conjuntoTitlesMassa {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;
  padding: 1rem;
}

.titleMassa {
  color: #092F47;
  font-weight: bold;
  font-size: 30px;
  display: flex;
  justify-content: flex-start;
  text-align: start;
}

.titleMassa2 {
  color: black;
  font-weight: bold;
  font-size: 15px;
}

.toolbarContent {
  background: rgb(255, 255, 255);
  display: flex;
  width: 100%;
  padding: 2rem;
}

.btnNavBar {
  color: black;
  font-size: 16px;
  font-weight: 500;
  text-transform: none;
}
</style>