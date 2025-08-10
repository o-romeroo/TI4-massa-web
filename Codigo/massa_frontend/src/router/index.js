import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '../layouts/MainLayout.vue';
import Home from '../views/Home.vue';
import Algorithm from '../views/Algorithm.vue';
import About from '../views/About.vue';
import Support from '../views/Support.vue';
import Execution from '../views/Execution.vue';
import UserData from '../views/UserData.vue';
import Login from '../views/Login.vue';
import Register from '@/views/Register.vue';
import { useAuthStore } from '@/stores/auth';

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        component: Home,
        meta: {
          requiresAuth: false,
        }
      },
      {
        path: 'execution',
        component: Execution,
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: 'algorithm',
        component: Algorithm,
        meta: {
          requiresAuth: false,
        },
      },
      {
        path: 'about',
        component: About,
        meta: {
          requiresAuth: false,
        },
      },
      {
        path: 'support',
        component: Support,
        meta: {
          requiresAuth: false,
        },
      },
      {
        path: 'data',
        component: UserData,
        meta: {
          requiresAuth: false,
        },
      },
      {
        path: 'login',
        component: Login,
        meta: {
          requiresAuth: false,
        },
      },
      {
        path: 'register',
        component: Register,
        meta: {
          requiresAuth: false,
        },
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ path: '/login', query: { redirect: to.fullPath } });
  } else {
    next();
  }
});

export default router;