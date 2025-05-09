import { createRouter, createWebHistory } from 'vue-router'
import BookList from '../components/BookList.vue'
import BorrowForm from '../components/BorrowForm.vue'
import TransactionList from '../components/TransactionList.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'

const routes = [
  { path: '/', component: BookList, meta: { requiresAuth: true } },
  { path: '/borrow', component: BorrowForm, meta: { requiresAuth: true } },
  { path: '/transactions', component: TransactionList, meta: { requiresAuth: true } },

  { path: '/login', component: Login },
  { path: '/register', component: Register },

  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
