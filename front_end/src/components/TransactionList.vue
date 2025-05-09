<template>
    <div class="container mt-5 p-5">
      <NavBar />
      <h2>Transactions</h2>
  
      <div v-if="isLoading" class="text-center my-5">
        <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>
      </div>
  
      <table class="table table-striped text-center align-items-center">
        <thead>
          <tr>
            <th>#</th>
            <th>Book</th>
            <th>Status</th>
            <th>Borrowed Date</th>
            <th>Returned</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in transactions" :key="t.id">
            <td>{{ t.id }}</td>
            <td>
              <div v-if="t.book.image">
                <a v-if="isImageFile(t.book.image)" :href="t.book.image" target="_blank">
                  <img :src="t.book.image" class="img-thumbnail" style="max-width: 60px;" />
                </a>
                <a v-else :href="t.book.image" target="_blank">View File</a>
              </div>
            </td>
            <td>
      
              <span v-if="t.status === 'returned'" class="badge bg-success">Returned</span>
              <span v-else class="badge bg-warning text-dark">Borrowed</span>
            </td>
            <td>{{ t.formatted_borrow_date }}</td>
            <td>{{ t.formatted_return_date || 'N/A' }}</td>
            <td>
              <!-- Only show the return button if the book hasn't been returned -->
              <button v-if="t.status !== 'returned'" class="btn btn-success btn-sm" @click="markReturned(t.id, t.book.id)">
  
                Return
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import Swal from 'sweetalert2'
  import { getTransactions, returnBook } from '../api'
  import NavBar from '../components/NavBar.vue'
  
  export default {
    components: { NavBar },
    data() {
      return { transactions: [], isLoading: false }
    },
    methods: {
      async fetchTransactions() {
        this.isLoading = true;
        try {
          const res = await getTransactions()
          this.transactions = res.data
        } catch (err) {
          Swal.fire('Error', err.response?.data?.error || 'Failed to load transactions.', 'error')
        } finally {
          this.isLoading = false
        }
      },
      async markReturned(transactionId, bookId) {
        try {
          await returnBook(transactionId, bookId)
  
          Swal.fire('Success', 'Book marked as returned.', 'success')
          this.fetchTransactions() // Refresh the transactions list after updating
        } catch (err) {
          Swal.fire('Error', err.response?.data?.error || 'Failed to mark book as returned.', 'error')
        }
      },
      isImageFile(filePath) {
        return filePath?.match(/\.(jpeg|jpg|gif|png|webp)$/i)
      }
    },
    mounted() {
      this.fetchTransactions()
    }
  }
  </script>
  
  <style scoped>
  .img-thumbnail {
    border: 1px solid #ccc;
  }
  
  table th, td {
    vertical-align: middle;
  }
  </style>
  