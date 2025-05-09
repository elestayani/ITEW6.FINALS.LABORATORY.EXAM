<template>
    <div class="container d-flex justify-content-center align-items-center vh-100">
      <div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%; border-radius: 12px;">
        <h2 class="text-center mb-4">Welcome Back</h2>
        <form @submit.prevent="login">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              v-model="username"
              class="form-control"
              id="username"
              placeholder="Enter your username"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              v-model="password"
              class="form-control"
              id="password"
              placeholder="Enter your password"
              required
            />
          </div>
          <div class="d-flex justify-content-between mb-3">
            <a href="#" class="text-decoration-none" @click="forgotPassword">Forgot Password?</a>
          </div>
          <button class="btn btn-primary w-100" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>
        <div class="text-center mt-3">
          <span>Don't have an account? </span>
          <a href="/register" class="text-decoration-none">Register here</a>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Swal from 'sweetalert2'
  import axios from 'axios'
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        loading: false,
      }
    },
    methods: {
      async login() {
        this.loading = true
        try {
          const response = await axios.post('http://localhost:8000/api/login/', {
            username: this.username,
            password: this.password
          })
  
          Swal.fire('Success', 'Login successful!', 'success')
  
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('user_id', response.data.user_id)
          this.$router.push('/')
        } catch (err) {
          const msg = err.response?.data?.error || 'Invalid credentials. Please try again.'
          Swal.fire('Login Failed', msg, 'error')
        } finally {
          this.loading = false
        }
      },
  
      forgotPassword() {
        Swal.fire('Reset your password', 'Please contact support to reset your password.', 'info')
      }
    }
  }
  </script>
  
  <style scoped>
  .container {
    background-color: #f8f9fa;
  }
  
  .card {
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  input:focus {
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  }
  
  a {
    color: #0d6efd;
    font-size: 0.9rem;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>
  