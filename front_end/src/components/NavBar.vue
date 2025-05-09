<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Library System</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Books</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/borrow">Borrow</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/transactions">Transactions</router-link>
            </li>
          </ul>
          <button @click="logout" class="btn btn-outline-light btn-sm">Logout</button>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    methods: {
      logout() {
        localStorage.removeItem('token')
        localStorage.removeItem('user_id')
        localStorage.removeItem('username')
        this.$router.push('/login')
        this.$router.push('/login')
      },
      computed: {
        isLoggedIn() {
            return !!localStorage.getItem('token')
        }
        }
    }
  }
  </script>

  <style scoped>
  nav{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
  }
  </style>
  