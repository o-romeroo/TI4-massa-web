<template>
    <v-card class="mx-auto" elevation="1" max-width="500">
      <!-- <v-card-title class="py-5 font-weight-black">
        <v-row>
          <v-col cols="1" class="ps-3">
            <v-btn icon="mdi-chevron-left" @click="$router.push('/login')" variant="plain">
            </v-btn>
          </v-col>
          
          <v-col class=" justify-center pt-4 ps-8">
            Register in Massa Software
          </v-col>
        </v-row>
      </v-card-title> -->

      <v-card-title class="py-5 font-weight-black text-center justify-center">
        Register in Massa Software
    </v-card-title>
  
      <v-card-text>
        <div class="text-subtitle-2 font-weight-black mb-1">Username</div>
  
        <v-text-field
          v-model="userData.username"
          prepend-inner-icon="mdi-account-outline"
          :rules="[rules.required, rules.usernameValid]"
          label="Insert your username"
          variant="outlined"
          single-line
        ></v-text-field>
        <div style="margin-bottom: 0.5rem;"></div>
  
        <div class="text-subtitle-2 font-weight-black mb-1">Email</div>
  
        <v-text-field
          v-model="userData.email"
          prepend-inner-icon="mdi-email-outline"
          :rules="[rules.required, rules.emailValid]"
          label="Insert your email"
          variant="outlined"
          single-line
        ></v-text-field>
        <div style="margin-bottom: 0.5rem;"></div>
  
        <div class="text-subtitle-2 font-weight-black mb-1">Password</div>
        <v-text-field
          v-model="userData.password"
          :append-inner-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules.required, rules.min]"
          :type="show1 ? 'text' : 'password'"
          class="input-group--focused"
          hint="At least 8 characters"
          label="Insert your password"
          variant="outlined"
          single-line
          @click:append-inner="show1 = !show1"
        ></v-text-field>
  
        <v-text-field
          v-model="confirmPassword"
          :append-inner-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules.required, rules.min, rules.passwordMatch]"
          :type="show2 ? 'text' : 'password'"
          class="input-group--focused"
          hint="At least 8 characters"
          label="Confirm your password"
          variant="outlined"
          single-line
          @click:append-inner="show2 = !show2"
        ></v-text-field>
        <div style="margin-bottom: 0.5rem;"></div>
  
        <v-btn
          :disabled="loading"
          :loading="loading"
          class="text-none mb-4"
          color="#0A2E49"
          size="x-large"
          variant="flat"
          block
          @click="handleRegister()"
        >
          Register
        </v-btn>

        <v-btn
          class="text-none"
          color="grey-lighten-3"
          size="x-large"
          variant="flat"
          block
          to="/login"
        >
          Cancel
        </v-btn>

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

      </v-card-text>
    </v-card>
  </template>
  
  <script>
  import { useAuthStore } from '@/stores/auth';
  import { getIpInfos } from '@/services/Geolocation';
  
  export default {
    setup() {
      const authStore = useAuthStore();
  
      return { authStore };
    },
    data() {
      return {
        userData: {
          username: '',
          email: '',
          password: '',
          country: '',
          city: ''
        },
        show1: false,
        show2: false,
        confirmPassword: '',
        loading: false,
        showAlert: false,
        alertMessage: '',
        rules: {
          required: value => !!value || 'Required.',
          min: v => v.length >= 8 || 'Min 8 characters',
          emailValid: value => {
            const pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
            return pattern.test(value) || 'Invalid e-mail.';
          },
          passwordMatch: value => value === this.userData.password || 'Passwords do not match.',
          usernameValid: value => {
            const pattern = /^[a-zA-Z0-9_-]{4,16}$/;
            return pattern.test(value) || 'Invalid username.';
          }
        },
      };
    },
    methods: {
      async handleRegister() {
        this.loading = true;
        this.showAlert = false;

        const isUsernameValid = this.rules.required(this.userData.username) === true && this.rules.usernameValid(this.userData.username) === true;
        const isEmailValid = this.rules.required(this.userData.email) === true && this.rules.emailValid(this.userData.email) === true;
        const isPasswordValid = this.rules.required(this.userData.password) === true && this.rules.min(this.userData.password) === true;
        const isConfirmPasswordValid = this.rules.required(this.confirmPassword) === true && this.rules.min(this.confirmPassword) === true && this.rules.passwordMatch(this.confirmPassword) === true;

        if (!isUsernameValid || !isEmailValid || !isPasswordValid || !isConfirmPasswordValid) {
            this.alertMessage = 'Please fill in all fields correctly.';
            this.showAlert = true;
            this.loading = false;
            return;
        }
  
        const ipInfos = await getIpInfos();
  
        this.userData.country = ipInfos.country;
        this.userData.city = ipInfos.city;
  
        try {
          await this.authStore.register(this.userData);
          this.$router.push(this.$route.query.redirect || '/');
        } catch (error) {
            this.alertMessage = 'Register error.';
            this.showAlert = true;
          console.error("Register error:", error);
        } finally {
          this.loading = false;
        }
      }
    },
  };
  </script>
  