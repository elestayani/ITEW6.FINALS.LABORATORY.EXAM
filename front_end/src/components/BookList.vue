<template>
    <div class="container mt-5 p-5">
      <NavBar />
  
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">Books</h2>
        <button class="btn btn-primary" @click="openAddForm">Add Book</button>
      </div>
  
      <!-- Book Form Modal -->
      <div
        class="modal fade"
        :class="{ show: showForm }"
        :style="{ display: showForm ? 'block' : 'none' }"
        tabindex="-1"
        role="dialog"
      >
        <div class="modal-dialog modal-lg" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ editData ? 'Edit Book' : 'Add Book' }}</h5>
              <button type="button" class="btn-close" @click="closeForm" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="handleSubmit">
                <div class="mb-3">
                  <label class="form-label">Title</label>
                  <input v-model="form.title" type="text" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label class="form-label">Author</label>
                  <input v-model="form.author" type="text" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label class="form-label">ISBN</label>
                  <input v-model="form.isbn" type="text" class="form-control" required />
                </div>
  
                <div class="mb-4">
                  <label class="form-label">Copies Available</label>
                  <input v-model.number="form.copies_available" type="number" min="0" class="form-control" required />
                </div>
  
                <div class="mb-4">
                  <label class="form-label">Upload File</label>
                  <input type="file" class="form-control" @change="onFileChange" />
                  <div v-if="previewUrl" class="mt-3">
                    <p>Preview:</p>
                    <img v-if="isImage" :src="previewUrl" class="img-thumbnail" style="max-width: 200px;" />
                    <a v-else :href="previewUrl" target="_blank">View Uploaded File</a>
                  </div>
                </div>
  
                <div class="d-flex justify-content-end">
                  <button type="submit" class="btn btn-success">{{ editData ? 'Update Book' : 'Add Book' }}</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
  
      <div class="modal-backdrop fade" :class="{ show: showForm }" v-show="showForm"></div>
  
      <div v-if="isLoading" class="text-center my-5">
        <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>
      </div>
  
      <div class="table-responsive" v-else>
        <table class="table table-striped table-hover table-bordered align-middle">
          <thead class="table-dark">
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>ISBN</th>
              <th>Copies</th>
              <th>File</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in books" :key="book.id">
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td>{{ book.isbn }}</td>
              <td>{{ book.copies_available }}</td>
              <td>
                <div v-if="book.book">
                  <a v-if="isImageFile(book.book)" :href="book.book" target="_blank">
                    <img :src="book.book" class="img-thumbnail" style="max-width: 60px;" />
                  </a>
                  <a v-else :href="book.book" target="_blank">View File</a>
                </div>
              </td>
              <td class="text-center">
                <div class="btn-group" role="group">
                  <button class="btn btn-warning text-white btn-sm m-1" @click="editBook(book)">Edit</button>
                  <button class="btn btn-danger btn-sm m-1" @click="confirmDelete(book)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import Swal from 'sweetalert2'
  import { getBooks, createBook, updateBook, deleteBook } from '../api'
  import NavBar from './NavBar.vue'
  
  export default {
    components: { NavBar },
    data() {
      return {
        books: [],
        showForm: false,
        editData: null,
        isLoading: false,
        form: {
          title: '',
          author: '',
          isbn: '',
          copies_available: 0
        },
        file: null,
        previewUrl: ''
      }
    },
    computed: {
      isImage() {
        return this.previewUrl?.match(/\.(jpeg|jpg|png|gif|webp|bmp)$/i)
      }
    },
    methods: {
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
      openAddForm() {
        this.editData = null
        this.form = {
          title: '',
          author: '',
          isbn: '',
          copies_available: 0
        }
        this.file = null
        this.previewUrl = ''
        this.showForm = true
      },
      editBook(book) {
        this.editData = book
        this.form = { ...book }
        this.previewUrl = book.book || ''
        this.file = null
        this.showForm = true
      },
      closeForm() {
        this.showForm = false
        this.editData = null
        this.form = {
          title: '',
          author: '',
          isbn: '',
          copies_available: 0
        }
        this.file = null
        this.previewUrl = ''
      },
      onFileChange(e) {
        const file = e.target.files[0]
        if (file) {
          this.file = file
          this.previewUrl = URL.createObjectURL(file)
        }
      },
      async handleSubmit() {
        const formData = new FormData()
        formData.append('title', this.form.title)
        formData.append('author', this.form.author)
        formData.append('isbn', this.form.isbn)
        formData.append('copies_available', this.form.copies_available)
        if (this.file) {
          formData.append('book', this.file)
        }
  
        try {
          if (this.editData) {
            await updateBook(this.editData.id, formData)
            Swal.fire('Updated!', 'Book updated successfully.', 'success')
          } else {
            await createBook(formData)
            Swal.fire('Added!', 'Book added successfully.', 'success')
          }
          this.closeForm()
          this.fetchBooks()
        } catch (err) {
          Swal.fire('Error', err.response?.data?.error || 'Failed to save book.', 'error')
        }
      },
      async confirmDelete(book) {
        // Check if the book has an active borrower and if its status is 'borrowed'
        if (book.borrow && book.borrow.status === 'borrowed') {
          Swal.fire('Cannot Delete', 'This book is currently borrowed and cannot be deleted.', 'error')
          return
        }
  
        const result = await Swal.fire({
          title: 'Are you sure?',
          text: 'This will delete the book.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Yes, delete it!'
        })
  
        if (result.isConfirmed) {
          try {
            await deleteBook(book.id)
            Swal.fire('Deleted!', 'Book deleted successfully.', 'success')
            this.fetchBooks()
          } catch (err) {
            const message = err.response?.data?.error || 'Failed to delete book.'
            Swal.fire('Error', message, 'error')
          }
        }
      },
      isImageFile(filePath) {
        return filePath?.match(/\.(jpeg|jpg|png|gif|webp|bmp)$/i)
      }
    },
    mounted() {
      this.fetchBooks()
    }
  }
  </script>
  
  <style scoped>
  .img-thumbnail {
    border: 1px solid #ccc;
  }
  </style>
  