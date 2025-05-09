<template>
    <div class="container mt-5 p-5">
      <NavBar />
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">Borrow Book</h2>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#borrowModal">
          Borrow a Book
        </button>
      </div>
  
      <div class="modal fade" id="borrowModal" tabindex="-1" aria-labelledby="borrowModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <form @submit.prevent="borrow">
              <div class="modal-header">
                <h5 class="modal-title" id="borrowModalLabel">Borrow a Book</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <select v-model="userId" class="form-select mb-3" required>
                  <option disabled value="">-- Select a User --</option>
                  <option v-for="u in users" :value="u.id" :key="u.id">
                    Username: {{ u.username }} (User ID: {{ u.id }})
                  </option>
                </select>
  
                <select v-model="bookId" class="form-select" required>
                  <option disabled value="">Select Book</option>
                  <option v-for="b in books" :value="b.id" :key="b.id" :disabled="b.copies_available === 0">
                    {{ b.title }} ({{ b.copies_available }} available)
                  </option>
                </select>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Borrow</button>
              </div>
            </form>
          </div>
        </div>
      </div>
  
      <hr class="my-5" />
  
      <h3 class="mb-3">All Borrowing Transactions</h3>
      <div v-if="isLoading" class="text-center my-5">
        <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>
      </div>
      <div v-else class="table-responsive">
        <table class="table table-striped table-bordered align-middle">
          <thead class="table-dark">
            <tr>
              <th>User</th>
              <th>Book</th>
              <th>Status</th>
              <th>Borrowed</th>
              <th>Returned</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in transactions" :key="t.id">
              <td>{{ t.user }}</td>
              <td>
                <div>
                  {{ t.book.title }}
                  <div v-if="t.book.file">
                    <a v-if="!isImageFile(t.book.file)" :href="t.book.file" target="_blank" class="d-block small text-primary">View File</a>
                    <img v-else :src="t.book.file" class="img-thumbnail mt-1" style="max-width: 60px;" />
                  </div>
                </div>
              </td>
              <td>
                <span :class="t.status === 'returned' ? 'badge bg-success' : 'badge bg-warning text-dark'">
                  {{ t.status.charAt(0).toUpperCase() + t.status.slice(1) }}
                </span>
              </td>
              <td>{{ t.formatted_borrow_date }}</td>
              <td>{{ t.formatted_return_date || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import Swal from 'sweetalert2'
  import { borrowBook, getBooks, getTransactions } from '../api'
  import axios from 'axios'
  import NavBar from '../components/NavBar.vue'
  import 'bootstrap/dist/js/bootstrap.bundle.min.js'
  
  export default {
    components: { NavBar },
    data() {
      return {
        books: [],
        users: [],
        transactions: [],
        userId: '',
        bookId: '',
        isLoading: false,
      }
    },
    methods: {
      async borrow() {
        // Handle borrow API call separately
        try {
          await borrowBook({ user: this.userId, book: this.bookId })
          Swal.fire('Success', 'Book borrowed successfully.', 'success')
        } catch (err) {
          Swal.fire('Error', err.response?.data?.error || 'Failed to borrow book.', 'error')
          return
        }
  
        // UI updates after successful borrow
        this.userId = ''
        this.bookId = ''
        try {
          await this.fetchBooks()
          await this.fetchTransactions()
        } catch (err) {
          console.warn('Post-borrow data fetch failed:', err)
        }
  
        try {
          const modal = bootstrap.Modal.getInstance(document.getElementById('borrowModal'))
          modal?.hide()
        } catch (e) {
          console.warn('Modal hide failed:', e)
        }
      },
      async fetchBooks() {
        this.isLoading = true
        try {
          const res = await getBooks()
          this.books = res.data
        } catch (err) {
          Swal.fire('Error', err.response?.data?.error || 'Failed to load books.', 'error')
        } finally {
          this.isLoading = false
        }
      },
      async fetchUsers() {
        this.isLoading = true
        try {
          const res = await axios.get('http://localhost:8000/api/users/')
          this.users = res.data
        } catch (err) {
          Swal.fire('Error', err.response?.data?.error || 'Failed to load users.', 'error')
        } finally {
          this.isLoading = false
        }
      },
      async fetchTransactions() {
        const res = await getTransactions()
        this.transactions = res.data
      },
      isImageFile(filePath) {
        return filePath?.match(/\.(jpeg|jpg|png|gif)$/i)
      }
    },
    mounted() {
      this.fetchBooks()
      this.fetchUsers()
      this.fetchTransactions()
  
      // Fix for aria-hidden + focus warning
      const modalEl = document.getElementById('borrowModal')
      modalEl?.addEventListener('hidden.bs.modal', () => {
        if (document.activeElement && modalEl.contains(document.activeElement)) {
          document.activeElement.blur()
        }
      })
    }
  }
  </script>
  
  <style scoped>
  .img-thumbnail {
    max-height: 60px;
    border: 1px solid #ccc;
  }
  </style>
  