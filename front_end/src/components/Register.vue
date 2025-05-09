<template>
    <div class="container mt-5">
      <div class="card p-4 shadow-sm" style="max-width: 500px; margin: 0 auto; border-radius: 12px;">
        <h2 class="text-center mb-4">Register</h2>
        <form @submit.prevent="register">
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
            <a href="/login" class="text-decoration-none">Already have an account? Login</a>
          </div>
          <button class="btn btn-primary w-100" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? 'Registering...' : 'Register' }}
          </button>
        </form>
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
        loading: false
      }
    },
    methods: {
      async register() {
        this.loading = true
        try {
          const response = await axios.post('http://localhost:8000/api/register/', {
            username: this.username,
            password: this.password
          })
          Swal.fire('Success', 'Registration successful! You can now log in.', 'success')
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('user_id', response.data.user_id)
          this.$router.push('/login')
        } catch (err) {
          const msg = err.response?.data?.error || 'An error occurred'
          Swal.fire('Error', msg, 'error')
        } finally {
          this.loading = false
        }
      }
    }
  }
  </script>
  
  <style scoped>
  
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
  