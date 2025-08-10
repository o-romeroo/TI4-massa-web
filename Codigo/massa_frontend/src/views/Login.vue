<template>
    <v-card class="mx-auto" elevation="1" max-width="500">
        <v-card-title class="py-5 font-weight-black text-center justify-center">
      Login in Massa Software
    </v-card-title>
  
      <v-card-text>
        <div class="text-subtitle-2 font-weight-black mb-1">Username</div>
  
        <v-text-field
          v-model="username"
          prepend-inner-icon="mdi-account-outline"
          :rules="[rules.required, rules.usernameValid]"
          label="Insert your username"
          variant="outlined"
          single-line
        ></v-text-field>
  
        <div class="text-subtitle-2 font-weight-black mb-1 mt-4 d-flex align-center justify-space-between">
          Password
          <a
            class="text-caption text-decoration-none text-blue"
            href="#"
            rel="noopener noreferrer"
            target="_blank"
            >Forgot login password?</a
          >
        </div>
        <v-text-field
          v-model="password"
          :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules.required, rules.min]"
          :type="showPassword ? 'text' : 'password'"
          class="input-group--focused"
          hint="At least 8 characters"
          label="Insert your password"
          variant="outlined"
          @click:append-inner="showPassword = !showPassword"
        ></v-text-field>
  
        <v-btn
          :disabled="loading"
          :loading="loading"
          class="text-none mt-8 mb-4"
          color="#0A2E49"
          size="x-large"
          variant="flat"
          block
          @click="handleLogin()"
        >
          Login
        </v-btn>
  
        <v-btn
          class="text-none"
          color="grey-lighten-3"
          size="x-large"
          variant="flat"
          block
          to="/register"
        >
          Register
        </v-btn>
      </v-card-text>
  
      <v-snackbar
        v-model="showAlert"
        :timeout="4000"
        top
        multi-line
        color="error" 
        >
        {{ alertMessage }}
        <template v-slot:actions>
            <v-btn icon="mdi-close" variant="plain" @click="showAlert = false"/>
        </template>
        </v-snackbar>
        
    </v-card>
  </template>
  
  <script>
  import { useAuthStore } from '@/stores/auth';
  
  export default {
    setup() {
      const authStore = useAuthStore();
  
      return { authStore };
    },
    data() {
      return {
        showPassword: false,
        username: '',
        password: '',
        loading: false,
        showAlert: false,
        alertMessage: '',
        rules: {
          required: (value) => !!value || 'Required.',
          min: (v) => v.length >= 8 || 'Min 8 characters',
          usernameValid: (value) => {
            const pattern = /^[a-zA-Z0-9_-]{4,16}$/;
            return pattern.test(value) || 'Invalid username.';
          },
        },
      };
    },
    methods: {
      async handleLogin() {
        this.loading = true;
        this.showAlert = false; 
  
        const isUsernameValid = this.rules.required(this.username) === true && this.rules.usernameValid(this.username) === true;
        const isPasswordValid = this.rules.required(this.password) === true && this.rules.min(this.password) === true;
  
        if (!isUsernameValid || !isPasswordValid) {
          this.alertMessage = 'Please fill in the username and password correctly.';
          this.showAlert = true;
          this.loading = false;
          return;
        }
  
        try {
          await this.authStore.login(this.username, this.password);
          this.$router.push(this.$route.query.redirect || '/');
        } catch (error) {
          console.error('Login error:', error);
          this.alertMessage = 'Login error. Please check your credentials and try again.';
          this.showAlert = true;
        } finally {
          this.loading = false;
        }
      },
    },
  };
  </script>