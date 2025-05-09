<template>
    <NavBar>
        <div class="mt-5 p-5 card mb-3">
            <div class="card-body">
                <h5>{{ editData ? 'Edit Book' : 'Add Book' }}</h5>
                <form @submit.prevent="handleSubmit">
                <input v-model="book.title" class="form-control mb-2" placeholder="Title" required />
                <input v-model="book.author" class="form-control mb-2" placeholder="Author" required />
                <input v-model="book.isbn" class="form-control mb-2" placeholder="ISBN" required />
                <input v-model.number="book.copies_available" class="form-control mb-2" placeholder="Copies" type="number" min="0" required />
                <button class="btn btn-success" type="submit">{{ editData ? 'Update' : 'Create' }}</button>
                <button class="btn btn-secondary ms-2" @click.prevent="$emit('close')">Cancel</button>
                </form>
            </div>
        </div>
    </NavBar>
  </template>
  
  <script>
  import Swal from 'sweetalert2'
  import { createBook, updateBook } from '../api'
  import NavBar from '../components/NavBar.vue'
  
  export default {
    props: ['editData'],
    components: { NavBar },
    data() {
      return { book: { title: '', author: '', isbn: '', copies_available: 0 } }
    },
    watch: {
      editData: {
        immediate: true,
        handler(val) { if (val) this.book = { ...val } }
      }
    },
    methods: {
      async handleSubmit() {
        try {
          if (this.editData) {
            await updateBook(this.editData.id, this.book)
          } else {
            await createBook(this.book)
          }
          this.$emit('saved')
          Swal.fire('Success', 'Book saved successfully.', 'success')
        } catch (err) {
          Swal.fire('Error', 'Failed to save book.', 'error')
        }
      }
    }
  }
  </script>