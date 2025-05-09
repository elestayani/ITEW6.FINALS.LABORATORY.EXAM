import axios from 'axios'

const API = axios.create({ baseURL: 'http://localhost:8000/api/' })

const isFormData = (data) => data instanceof FormData

const config = (data) => ({
  headers: {
    'Content-Type': isFormData(data) ? 'multipart/form-data' : 'application/json'
  }
})

export const getBooks = () => API.get('books/')
export const createBook = (data) => API.post('books/', data, config(data))
export const updateBook = (id, data) => API.put(`books/${id}/`, data, config(data))
export const deleteBook = (id) => API.delete(`books/${id}/`)

export const borrowBook = (data) => API.post('borrow/', data, config(data))
export const returnBook = (borrowId) => API.post(`return/${borrowId}/`)
export const getTransactions = () => API.get('transactions/')
